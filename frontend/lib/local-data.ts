import { promises as fs } from "fs";
import path from "path";

type JsonValue = Record<string, any> | any[] | null;

const REPO_ROOT = path.resolve(process.cwd(), "..");
const DATA_ROOT = path.join(REPO_ROOT, "data");
const SRC_DATA_ROOT = path.join(REPO_ROOT, "src", "data");
const SNAPSHOT_ROOT = path.join(DATA_ROOT, "snapshots");

async function readJson<T = any>(filePath: string, fallback: T): Promise<T> {
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
    return { decisions: [] };
  }
  return readJson(path.join(SNAPSHOT_ROOT, latest, "snapshot.json"), { decisions: [] });
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
    };
  }
  return readJson(path.join(SNAPSHOT_ROOT, latest, "market_summary.json"), {
    total_stocks: 0,
    by_decision_zone: {},
    by_overall_risk: {},
    market_tone: "UNKNOWN",
    upgrades: 0,
    downgrades: 0,
  });
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
  return readJson(path.join(SRC_DATA_ROOT, "strategy_rankings", "strategy_rankings.json"), {
    generated_at: null,
    rankings: [],
  });
}

export async function getAlphaStrategiesLocal() {
  return readJson(
    path.join(SRC_DATA_ROOT, "generated_strategies", "generated_strategies.json"),
    { generated_at: null, strategies: [] }
  );
}

export async function getAlphaSignalsLocal() {
  return readJson(path.join(SRC_DATA_ROOT, "signals", "signals.json"), {
    generated_at: null,
    signals: [],
  });
}

export async function getAlphaMonitoringLocal() {
  return readJson(
    path.join(SRC_DATA_ROOT, "strategy_monitoring", "strategy_monitoring.json"),
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
  const stored = await readJson(path.join(DATA_ROOT, "signals", "top_opportunities.json"), [] as any[]);
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
  });
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
