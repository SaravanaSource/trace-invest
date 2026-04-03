import { promises as fs } from "fs";
import path from "path";

type JsonPrimitive = string | number | boolean | null;
type JsonValue = JsonPrimitive | JsonObject | JsonValue[];
type JsonObject = { [key: string]: JsonValue };

export type SnapshotDecision = {
  stock?: string;
  symbol?: string;
  decision_zone?: string;
  overall_risk?: string;
  conviction_score?: number;
  narrative?: string;
  valuation?: {
    valuation_sanity?: string;
  };
  governance?: {
    governance_band?: string;
    top_risks?: string[];
  };
  stability?: {
    stability_band?: string;
    weak_areas?: string[];
  };
  master?: {
    master_band?: string;
  };
  quality?: {
    confidence_band?: string;
  };
  delta?: {
    decision_change?: string;
    change_summary?: string;
  };
  system_awareness?: {
    confidence_level?: string;
    explanation?: string;
    missing_inputs?: string[];
  };
};

type SnapshotPayload = {
  run_date?: string;
  run_timestamp?: string;
  decisions?: SnapshotDecision[];
};

type MarketSummaryPayload = {
  total_stocks: number;
  by_decision_zone: Record<string, number>;
  by_overall_risk: Record<string, number>;
  upgrades: number;
  downgrades: number;
  market_tone: string;
  risk_increases?: number;
  risk_decreases?: number;
};

type AlphaPosition = {
  symbol: string;
  weight?: number;
};

type AlphaStrategyResult = {
  id: number;
  strategy: string;
  created_at: string | null;
  result: {
    strategy: string;
    score: number;
    CAGR?: number;
    sharpe_ratio?: number;
    max_drawdown?: number;
    volatility?: number;
    positions: AlphaPosition[];
  };
};

type AlphaResultsPayload = {
  results: AlphaStrategyResult[];
};

type AlphaSignal = {
  signal_name: string;
  symbol: string;
  signal_strength: number;
  explanation?: string;
};

type AlphaSignalsPayload = {
  generated_at: string | null;
  signals: AlphaSignal[];
};

type OpportunitySignal = {
  signal_name: string;
  signal_strength: number;
};

type OpportunityItem = {
  symbol: string;
  score: number;
  signals: OpportunitySignal[];
};

type HistoryPayload = {
  symbol: string;
  close?: number[];
  fundamentals?: {
    eps_quarterly?: number[];
  };
  insider?: {
    net_shares?: number;
  };
};

export type ValueCandidate = {
  symbol: string;
  score: number;
  alpha_score: number;
  strategy_count: number;
  signal_count: number;
  average_signal_strength: number;
  price_change_pct: number | null;
  recent_change_pct: number | null;
  valuation_view: string;
  risk_level: string;
  decision_zone: string;
  confidence: string;
  reasons: string[];
  risks: string[];
  narrative: string;
};

export type MarketPulse = {
  as_of: string | null;
  tone: string;
  headline: string;
  summary: string;
  action: string;
  breadth_view: string;
  risk_view: string;
  leadership_view: string;
  evidence: string[];
  pinned_stock: ValueCandidate | null;
  candidates: ValueCandidate[];
};

const REPO_ROOT = path.resolve(process.cwd(), "..");
const DATA_ROOT = path.join(REPO_ROOT, "data");
const TRACE_ARTIFACT_ROOT = path.join(REPO_ROOT, "src", "trace_invest", "data");
const SOURCE_DATA_ROOT = path.join(REPO_ROOT, "src", "data");
const SNAPSHOT_ROOT = path.join(DATA_ROOT, "snapshots");
const FRONTEND_ROOT = process.cwd();

async function readJson<T>(filePath: string, fallback: T): Promise<T> {
  try {
    const raw = await fs.readFile(filePath, "utf8");
    return JSON.parse(raw) as T;
  } catch {
    return fallback;
  }
}

async function writeJson(filePath: string, payload: JsonValue) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.writeFile(filePath, JSON.stringify(payload, null, 2), "utf8");
}

function normalizeSymbol(symbol: string) {
  return symbol.replace(/\.[A-Z]+$/i, "").trim().toUpperCase();
}

function startCaseSignal(signal: string) {
  return signal
    .split("_")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

function clamp(value: number, min: number, max: number) {
  return Math.min(max, Math.max(min, value));
}

function round(value: number) {
  return Math.round(value * 10) / 10;
}

function percentageChange(start: number, end: number) {
  if (!Number.isFinite(start) || start === 0 || !Number.isFinite(end)) {
    return null;
  }
  return ((end - start) / start) * 100;
}

function computeVolatility(closes: number[]) {
  if (closes.length < 3) {
    return null;
  }

  const returns = closes.slice(1).map((price, index) => {
    const previous = closes[index];
    return previous === 0 ? 0 : (price - previous) / previous;
  });

  const mean = returns.reduce((sum, value) => sum + value, 0) / returns.length;
  const variance =
    returns.reduce((sum, value) => sum + (value - mean) ** 2, 0) / returns.length;

  return Math.sqrt(variance);
}

async function listSnapshotDates() {
  try {
    const entries = await fs.readdir(SNAPSHOT_ROOT, { withFileTypes: true });
    return entries
      .filter((entry) => entry.isDirectory())
      .map((entry) => entry.name)
      .sort();
  } catch {
    return [];
  }
}

function normalizeWatchlists(raw: Record<string, string[]> | null | undefined) {
  const input = raw || {};
  return {
    watchlists: Object.entries(input).map(([name, symbols], index) => ({
      id: index + 1,
      name,
      symbols: Array.isArray(symbols) ? symbols : [],
    })),
  };
}

function toReasoningFilename(symbol: string) {
  return `${symbol.replace(/\./g, "_").toUpperCase()}.json`;
}

export async function getLatestSnapshotLocal() {
  const dates = await listSnapshotDates();
  const latest = dates.at(-1);
  if (!latest) {
    return { decisions: [] } as SnapshotPayload;
  }
  return readJson(path.join(SNAPSHOT_ROOT, latest, "snapshot.json"), {
    decisions: [],
  } as SnapshotPayload);
}

export async function getMarketSummaryLocal() {
  const dates = await listSnapshotDates();
  const latest = dates.at(-1);
  if (!latest) {
    return {
      total_stocks: 0,
      by_decision_zone: {},
      by_overall_risk: {},
      market_tone: "UNKNOWN",
      upgrades: 0,
      downgrades: 0,
    } as MarketSummaryPayload;
  }
  return readJson(path.join(SNAPSHOT_ROOT, latest, "market_summary.json"), {
    total_stocks: 0,
    by_decision_zone: {},
    by_overall_risk: {},
    market_tone: "UNKNOWN",
    upgrades: 0,
    downgrades: 0,
  } as MarketSummaryPayload);
}

export async function getStockReasoningLocal(symbol: string) {
  const dates = await listSnapshotDates();
  const latest = dates.at(-1);
  if (!latest) {
    return {
      metadata: { stock: symbol, symbol, run_date: null },
      evaluation_scope: { categories: [] },
      observed_facts: {},
      interpretation_rules: [],
      aggregation_logic: {},
      delta_interpretation: {},
      final_verdict: {},
      verification_guidance: [],
    };
  }

  const story = await readJson(
    path.join(SNAPSHOT_ROOT, latest, "reasoning", toReasoningFilename(symbol)),
    null
  );
  if (story) {
    return story;
  }

  const snapshot = await getLatestSnapshotLocal();
  const decision: any = (snapshot.decisions || []).find((item: any) => {
    const stock = String(item.stock || "").toUpperCase();
    const sym = String(item.symbol || "").toUpperCase();
    const requested = symbol.toUpperCase();
    return stock === requested || sym === requested;
  });

  return {
    metadata: { stock: decision?.stock || symbol, symbol, run_date: latest },
    evaluation_scope: { categories: ["governance", "stability", "valuation", "risk"] },
    observed_facts: {
      governance: (decision?.governance?.top_risks || []).map((risk: string) => ({
        name: risk,
        status: "FLAGGED",
        risk: decision?.overall_risk || "UNKNOWN",
        explanation: "Derived from the latest snapshot because a full reasoning file was unavailable.",
      })),
      stability: (decision?.stability?.weak_areas || []).map((risk: string) => ({
        name: risk,
        status: "WEAK",
        risk: decision?.overall_risk || "UNKNOWN",
      })),
    },
    interpretation_rules: [],
    aggregation_logic: {
      decision_zone: decision?.decision_zone,
      overall_risk: decision?.overall_risk,
    },
    delta_interpretation: decision?.delta || {},
    final_verdict: {
      decision_zone: decision?.decision_zone,
      overall_risk: decision?.overall_risk,
      primary_reasons: [decision?.narrative].filter(Boolean),
    },
    verification_guidance: [
      "Review the latest snapshot narrative.",
      "Check the source fundamentals and price history before acting.",
    ],
  };
}

export async function getAlphaRankingsLocal() {
  return readJson(path.join(TRACE_ARTIFACT_ROOT, "strategy_rankings", "strategy_rankings.json"), {
    generated_at: null,
    rankings: [],
  });
}

export async function getAlphaStrategiesLocal() {
  return readJson(
    path.join(TRACE_ARTIFACT_ROOT, "generated_strategies", "generated_strategies.json"),
    { generated_at: null, strategies: [] }
  );
}

export async function getAlphaSignalsLocal() {
  return readJson(path.join(SOURCE_DATA_ROOT, "signals", "signals.json"), {
    generated_at: null,
    signals: [],
  } as AlphaSignalsPayload);
}

export async function getAlphaMonitoringLocal() {
  return readJson(
    path.join(TRACE_ARTIFACT_ROOT, "strategy_monitoring", "strategy_monitoring.json"),
    { generated_at: null, items: [] }
  );
}

export async function getAlphaResultsLocal() {
  const rankings = await getAlphaRankingsLocal();
  const strategies = await getAlphaStrategiesLocal();

  const results = (rankings.rankings || []).map((ranking: any, index: number) => {
    const strategy: any = (strategies.strategies || []).find(
      (item: any) => item.strategy_name === ranking.strategy
    );
    return {
      id: index + 1,
      strategy: ranking.strategy,
      created_at: rankings.generated_at || strategy?.created_at || null,
      result: {
        strategy: ranking.strategy,
        score: ranking.alpha_score,
        CAGR: ranking.CAGR,
        sharpe_ratio: ranking.sharpe,
        max_drawdown: ranking.max_drawdown,
        volatility: ranking.volatility,
        positions: strategy?.positions || [],
      },
    };
  });

  const hasPositions = results.some((entry: any) => entry.result.positions.length > 0);
  if (hasPositions) {
    return { results } as AlphaResultsPayload;
  }

  const packaged = await readJson<AlphaResultsPayload>(
    path.join(FRONTEND_ROOT, "product_alpha_results.json"),
    { results: [] }
  );
  if ((packaged.results || []).length > 0) {
    return packaged;
  }

  return { results };
}

export async function getAlertsLocal() {
  const stored = await readJson(path.join(DATA_ROOT, "alerts", "alerts.json"), [] as any[]);
  if (Array.isArray(stored) && stored.length > 0) {
    return stored;
  }

  const snapshot = await getLatestSnapshotLocal();
  return (snapshot.decisions || [])
    .filter(
      (item: any) =>
        item.overall_risk === "HIGH" || item.delta?.decision_change === "DOWNGRADE"
    )
    .map((item: any) => ({
      symbol: item.symbol || item.stock,
      alert_type: item.delta?.decision_change === "DOWNGRADE" ? "Downgrade" : "High Risk",
      severity: item.overall_risk || "MEDIUM",
      reason:
        item.delta?.change_summary ||
        item.narrative ||
        "Latest snapshot flagged this stock for review.",
      message:
        item.delta?.change_summary ||
        item.narrative ||
        "Latest snapshot flagged this stock for review.",
    }));
}

export async function getOpportunitiesLocal() {
  const stored = await readJson(path.join(DATA_ROOT, "signals", "top_opportunities.json"), [] as OpportunityItem[]);
  if (Array.isArray(stored) && stored.some((item) => (item.signals || []).length > 0 || item.score > 0)) {
    return stored;
  }

  const signals = await getAlphaSignalsLocal();
  const rankings = await getAlphaRankingsLocal();
  const strategies = await getAlphaStrategiesLocal();

  return (rankings.rankings || []).slice(0, 5).flatMap((ranking: any) => {
    const strategy: any = (strategies.strategies || []).find(
      (item: any) => item.strategy_name === ranking.strategy
    );
    return (strategy?.positions || []).map((position: any) => ({
      symbol: position.symbol,
      score: ranking.alpha_score,
      signals: (signals.signals || [])
        .filter((signal: any) => signal.symbol === position.symbol)
        .map((signal: any) => ({
          signal_name: signal.signal_name,
          signal_strength: signal.signal_strength,
        })),
    }));
  }).concat(await getPackagedOpportunitiesLocal());
}

export async function getPortfolioLocal() {
  const direct = await readJson(path.join(DATA_ROOT, "portfolio.json"), null);
  const nested = await readJson(path.join(DATA_ROOT, "portfolio", "portfolio.json"), null);
  const raw = direct || nested || { cash: 0, positions: {} };

  const positionsObject = raw.positions;
  if (positionsObject && !Array.isArray(positionsObject) && Object.keys(positionsObject).length > 0) {
    return {
      cash: raw.cash || 0,
      positions: Object.entries(positionsObject).map(([symbol, details]: [string, any]) => ({
        symbol,
        weight: details?.weight || details?.quantity || 0,
      })),
    };
  }

  if (Array.isArray(raw.positions) && raw.positions.length > 0) {
    return { cash: raw.cash || 0, positions: raw.positions };
  }

  const results = await getAlphaResultsLocal();
  const top = results.results[0]?.result?.positions || [];
  return {
    cash: 0,
    positions: top.map((position: any) => ({
      symbol: position.symbol,
      weight: position.weight,
    })),
  };
}

export async function getWatchlistsLocal() {
  const stored = await readJson(path.join(DATA_ROOT, "watchlists", "long_term.json"), {});
  return normalizeWatchlists(stored);
}

export async function createWatchlistLocal(payload: {
  name: string;
  symbols: string[];
}) {
  const filePath = path.join(DATA_ROOT, "watchlists", "long_term.json");
  const stored = await readJson<Record<string, string[]>>(filePath, {});
  stored[payload.name] = payload.symbols;
  await writeJson(filePath, stored);
  return {
    id: Object.keys(stored).length,
    name: payload.name,
    symbols: payload.symbols,
  };
}

export async function getAdminMetricsLocal() {
  const rankings = await getAlphaRankingsLocal();
  const snapshotDates = await listSnapshotDates();
  return {
    strategy_results: (rankings.rankings || []).length,
    queue_length: 0,
    snapshot_count: snapshotDates.length,
    latest_snapshot: snapshotDates.at(-1) || null,
    source: "local_artifacts",
  };
}

async function getPackagedOpportunitiesLocal() {
  const packagedResults = await readJson<AlphaResultsPayload>(
    path.join(FRONTEND_ROOT, "product_alpha_results.json"),
    { results: [] }
  );
  const signals = await getAlphaSignalsLocal();
  const signalItems = signals.signals as AlphaSignal[];

  return packagedResults.results.flatMap((result) => {
    const positions = (result.result.positions || []) as AlphaPosition[];
    return positions.map((position: AlphaPosition) => {
      const symbol = position.symbol;
      const matchingSignals = signalItems
        .filter((signal) => normalizeSymbol(signal.symbol) === normalizeSymbol(symbol))
        .map((signal) => ({
          signal_name: signal.signal_name,
          signal_strength: signal.signal_strength,
        }));

      return {
        symbol,
        score: Number(result.result.score || 0),
        signals: matchingSignals,
      };
    });
  });
}

async function getHistoryLocal(symbol: string) {
  return readJson<HistoryPayload>(
    path.join(SOURCE_DATA_ROOT, "history", `${normalizeSymbol(symbol)}.json`),
    { symbol: normalizeSymbol(symbol) }
  );
}

async function buildValueCandidatesLocal(): Promise<ValueCandidate[]> {
  const opportunities = await getOpportunitiesLocal();
  const snapshot = await getLatestSnapshotLocal();
  const decisionMap = new Map(
    (snapshot.decisions || []).map((decision) => [
      normalizeSymbol(decision.symbol || decision.stock || ""),
      decision,
    ])
  );

  const aggregate = new Map<
    string,
    {
      symbol: string;
      alphaScore: number;
      strategyCount: number;
      signals: Map<string, number>;
    }
  >();

  for (const item of opportunities) {
    const key = normalizeSymbol(item.symbol);
    const current = aggregate.get(key) || {
      symbol: key,
      alphaScore: 0,
      strategyCount: 0,
      signals: new Map<string, number>(),
    };

    current.alphaScore += Number(item.score || 0);
    current.strategyCount += 1;

    for (const signal of item.signals || []) {
      const previous = current.signals.get(signal.signal_name) || 0;
      current.signals.set(
        signal.signal_name,
        Math.max(previous, Number(signal.signal_strength || 0))
      );
    }

    aggregate.set(key, current);
  }

  const candidates: ValueCandidate[] = [];

  for (const entry of aggregate.values()) {
    const history = await getHistoryLocal(entry.symbol);
    const closes = history.close || [];
    const eps = history.fundamentals?.eps_quarterly || [];
    const decision = decisionMap.get(entry.symbol);
    const signalEntries = Array.from(entry.signals.entries()).sort((a, b) => b[1] - a[1]);
    const averageSignalStrength =
      signalEntries.length === 0
        ? 0
        : signalEntries.reduce((sum, [, strength]) => sum + strength, 0) / signalEntries.length;
    const fullReturn = closes.length > 1 ? percentageChange(closes[0], closes[closes.length - 1]) : null;
    const recentReturn =
      closes.length > 5 ? percentageChange(closes[closes.length - 6], closes[closes.length - 1]) : null;
    const epsGrowth =
      eps.length > 1 ? percentageChange(eps[0], eps[eps.length - 1]) : null;
    const volatility = computeVolatility(closes);
    const hasInsider = signalEntries.some(([signal]) => signal === "insider_accumulation");
    const hasEarnings = signalEntries.some(([signal]) => signal === "earnings_acceleration");
    const hasMomentum = signalEntries.some(([signal]) => signal === "momentum_breakout");
    const hasLowVolatility = signalEntries.some(([signal]) => signal === "volatility_drop");

    let score = Math.min(entry.alphaScore / 240, 45);
    score += averageSignalStrength * 20;
    score += Math.min(signalEntries.length * 4, 16);
    score += hasInsider ? 10 : 0;
    score += hasEarnings ? 9 : 0;
    score += hasMomentum ? 7 : 0;
    score += hasLowVolatility ? 6 : 0;
    score += epsGrowth !== null && epsGrowth > 20 ? 10 : epsGrowth !== null && epsGrowth > 5 ? 5 : 0;
    score += recentReturn !== null && recentReturn > 0 ? 4 : 0;
    score += volatility !== null && volatility < 0.01 ? 7 : volatility !== null && volatility < 0.02 ? 4 : 0;

    const valuationView = String(decision?.valuation?.valuation_sanity || "UNSPECIFIED").toUpperCase();
    if (valuationView === "REASONABLE") {
      score += 8;
    }
    if (valuationView === "CHEAP") {
      score += 12;
    }
    if (valuationView === "RICH") {
      score -= 10;
    }

    const riskLevel = String(decision?.overall_risk || "MEDIUM").toUpperCase();
    if (riskLevel === "HIGH") {
      score -= 18;
    }
    if (riskLevel === "LOW") {
      score += 4;
    }

    const confidence = String(
      decision?.quality?.confidence_band ||
        (signalEntries.length >= 3 ? "HIGH" : signalEntries.length >= 2 ? "MEDIUM" : "LOW")
    ).toUpperCase();

    const reasons: string[] = [];
    if (hasInsider) {
      reasons.push("Insider accumulation is present, which strengthens the setup.");
    }
    if (hasEarnings && epsGrowth !== null) {
      reasons.push(`Quarterly EPS is accelerating, up ${round(epsGrowth)}% across the sample.`);
    }
    if (hasMomentum && fullReturn !== null) {
      reasons.push(`Price trend is constructive, with roughly ${round(fullReturn)}% appreciation in the local history.`);
    }
    if (hasLowVolatility) {
      reasons.push("Volatility remains contained, so the move is not purely chaotic.");
    }
    if (valuationView === "REASONABLE") {
      reasons.push("Latest valuation read is still reasonable, which keeps the idea investable.");
    }
    if (reasons.length === 0) {
      reasons.push("Multiple ranked strategies still surface this name as one of the cleaner current setups.");
    }

    const risks: string[] = [];
    if (riskLevel === "HIGH") {
      risks.push("Latest snapshot still flags elevated overall risk.");
    }
    if (decision?.governance?.top_risks?.length) {
      risks.push(`Governance watchpoint: ${decision.governance.top_risks[0]}.`);
    }
    if (decision?.stability?.weak_areas?.length) {
      risks.push(`Stability watchpoint: ${decision.stability.weak_areas[0]}.`);
    }
    if (decision?.system_awareness?.missing_inputs?.length) {
      risks.push("Some core inputs are missing, so this read should be treated as provisional.");
    }
    if (recentReturn !== null && recentReturn > 12) {
      risks.push("Short-term move is already strong, so wait for a disciplined entry.");
    }
    if (risks.length === 0) {
      risks.push("No full governance packet exists for this local sample, so fundamentals still need manual confirmation.");
    }

    const decisionZone = String(decision?.decision_zone || "WATCH").toUpperCase();
    const narrative =
      reasons[0] ||
      decision?.narrative ||
      "Current signals suggest this stock is one of the more attractive names in the local universe.";

    candidates.push({
      symbol: entry.symbol,
      score: round(clamp(score, 0, 100)),
      alpha_score: round(entry.alphaScore),
      strategy_count: entry.strategyCount,
      signal_count: signalEntries.length,
      average_signal_strength: round(averageSignalStrength),
      price_change_pct: fullReturn === null ? null : round(fullReturn),
      recent_change_pct: recentReturn === null ? null : round(recentReturn),
      valuation_view: valuationView,
      risk_level: riskLevel,
      decision_zone: decisionZone,
      confidence,
      reasons: reasons.slice(0, 3),
      risks: risks.slice(0, 3),
      narrative,
    });
  }

  return candidates.sort((left, right) => right.score - left.score);
}

export async function getMarketPulseLocal(): Promise<MarketPulse> {
  const summary = await getMarketSummaryLocal();
  const snapshot = await getLatestSnapshotLocal();
  const candidates = await buildValueCandidatesLocal();
  const pinned = candidates[0] || null;
  const latestDecision = (snapshot.decisions || [])[0];
  const tone = String(summary.market_tone || "UNKNOWN").toUpperCase();
  const highRisk = summary.by_overall_risk.HIGH || 0;
  const total = summary.total_stocks || 0;
  const riskRatio = total > 0 ? round((highRisk / total) * 100) : 0;

  const breadthView =
    Object.keys(summary.by_decision_zone || {}).length === 0
      ? "Breadth is unavailable from the current snapshot."
      : Object.entries(summary.by_decision_zone)
          .map(([zone, count]) => `${zone}: ${count}`)
          .join(" | ");

  const riskView =
    Object.keys(summary.by_overall_risk || {}).length === 0
      ? "Risk mix is unavailable from the current snapshot."
      : Object.entries(summary.by_overall_risk)
          .map(([risk, count]) => `${risk}: ${count}`)
          .join(" | ");

  const leadershipSignals = candidates
    .flatMap((candidate) => candidate.reasons)
    .slice(0, 3)
    .join(" ");

  let headline = "Market is mixed, so selective positioning matters most.";
  let summaryText =
    "Use the current snapshot as a narrow decision tool rather than a broad market-wide signal.";
  let action = "Stay selective and focus only on the cleanest stock-level setup.";

  if (tone === "CAUTIOUS") {
    headline = "Market is defensive right now, with risk staying elevated.";
    summaryText = `The latest snapshot tracks ${total} stock${total === 1 ? "" : "s"}, with ${riskRatio}% sitting in HIGH risk and downgrades outnumbering upgrades.`;
    action = pinned
      ? `Do not buy broadly. If you want one focused idea to research, start with ${pinned.symbol} and keep position sizing disciplined.`
      : "Do not buy broadly until breadth improves.";
  } else if (tone === "CONSTRUCTIVE" || tone === "BULLISH") {
    headline = "Market tone is improving and the stronger ideas deserve attention.";
    summaryText = `Upgrades are leading downgrades, which supports looking for individual names with improving fundamentals and contained risk.`;
    action = pinned
      ? `Lean into the strongest setup, currently ${pinned.symbol}, while monitoring any change in risk tone.`
      : "Lean into the strongest ranked names while monitoring risk.";
  }

  if (latestDecision?.delta?.change_summary) {
    summaryText += ` Latest change: ${latestDecision.delta.change_summary}`;
  }

  return {
    as_of: snapshot.run_date || snapshot.run_timestamp || null,
    tone,
    headline,
    summary: summaryText,
    action,
    breadth_view: breadthView,
    risk_view: riskView,
    leadership_view:
      leadershipSignals || "Leadership is currently being driven by multi-signal setups rather than broad breadth.",
    evidence: [
      `Coverage: ${summary.total_stocks} stock${summary.total_stocks === 1 ? "" : "s"} in the latest snapshot.`,
      `Decision mix: ${breadthView}.`,
      `Risk mix: ${riskView}.`,
      `Changes: ${summary.upgrades} upgrade(s), ${summary.downgrades} downgrade(s).`,
    ],
    pinned_stock: pinned,
    candidates: candidates.slice(0, 5),
  };
}
