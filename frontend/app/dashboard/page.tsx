import Link from "next/link";
import { Card } from "@/components/ui/Card";
import { getAlerts, getAlphaResults, getMarketSummary } from "@/lib/api";

type MarketSummary = {
  total_stocks: number;
  by_decision_zone: Record<string, number>;
  by_overall_risk: Record<string, number>;
  upgrades?: number;
  downgrades?: number;
  market_tone?: string;
};

export default async function Dashboard() {
  const summary: MarketSummary = await getMarketSummary();
  const alphaResponse = await getAlphaResults();
  const alerts = await getAlerts();

  const alpha = (alphaResponse?.results || []).flatMap((entry: any) => {
    const positions = Array.isArray(entry.result?.positions) ? entry.result.positions : [];
    if (positions.length === 0) {
      return [];
    }

    return positions.map((position: any) => ({
      symbol: position.symbol,
      name: position.name || "",
      summary: entry.strategy || entry.result?.strategy || "",
      score: entry.result?.score || 0,
      confidence: Number(entry.result?.score || 0) >= 20 ? "High" : "Medium",
    }));
  });

  const tone = (summary.market_tone || "UNKNOWN").toUpperCase();
  const toneExplainer =
    tone === "CAUTIOUS"
      ? "Market showing uncertainty - avoid aggressive positions."
      : tone === "BULLISH"
        ? "Market showing strength - prioritize high-conviction ideas."
        : tone === "BEARISH"
          ? "Market trending lower - favor risk management and cash."
          : "Mixed signals - focus on high-confidence opportunities.";

  return (
    <div className="max-w-5xl space-y-6 p-6">
      <h1 className="text-3xl font-bold">Daily Control Center</h1>
      <div className="text-sm text-white/70">AI-powered signals updated weekly</div>

      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <div className="text-sm text-white/60">Market tone</div>
          <div className="mt-2 text-2xl font-bold">{tone}</div>
          <div className="mt-2 text-sm text-textSecondary">{toneExplainer}</div>
        </Card>
        <Card>
          <div className="text-sm text-white/60">Coverage</div>
          <div className="mt-2 text-2xl font-bold">{summary.total_stocks}</div>
          <div className="mt-2 text-sm text-textSecondary">stocks in latest snapshot</div>
        </Card>
        <Card>
          <div className="text-sm text-white/60">Upgrades</div>
          <div className="mt-2 text-2xl font-bold">{summary.upgrades || 0}</div>
          <div className="mt-2 text-sm text-textSecondary">decision improvements</div>
        </Card>
        <Card>
          <div className="text-sm text-white/60">Downgrades</div>
          <div className="mt-2 text-2xl font-bold">{summary.downgrades || 0}</div>
          <div className="mt-2 text-sm text-textSecondary">names to review carefully</div>
        </Card>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <div className="md:col-span-2">
          <Card>
            <div className="text-sm text-white/60">What you should do today</div>
            <ul className="mt-3 ml-5 list-disc space-y-2 text-sm">
              <li>Prioritize the top ranked ideas before scanning the full universe.</li>
              <li>Review any high-risk or downgraded names in alerts.</li>
              <li>Use stock reasoning pages before adding anything to a watchlist.</li>
            </ul>
          </Card>
        </div>

        <Card>
          <div className="text-sm text-white/60">Current posture</div>
          <div className="mt-3 space-y-2 text-sm text-textSecondary">
            <div>Decision zones: {Object.entries(summary.by_decision_zone || {}).map(([key, value]) => `${key} ${value}`).join(", ") || "No data"}</div>
            <div>Risk mix: {Object.entries(summary.by_overall_risk || {}).map(([key, value]) => `${key} ${value}`).join(", ") || "No data"}</div>
          </div>
        </Card>
      </div>

      <div>
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-semibold">Top opportunities right now</h2>
          <div className="text-sm text-white/60">Alpha Lab - ranked from local artifacts</div>
        </div>

        <div className="mt-4 space-y-4">
          {alpha.slice(0, 3).map((idea: any, index: number) => {
            const isTop = index === 0;
            const numericScore = Number(idea.score || 0);
            return (
              <div
                key={`${idea.symbol}-${index}`}
                className={`card-bg rounded-xl border border-borderSoft p-6 transition-transform ${
                  isTop ? "scale-105 ring-4 ring-yellow-400/20" : ""
                }`}
              >
                <div className="flex items-start justify-between">
                  <div>
                    <div className="text-sm muted">#{index + 1}</div>
                    <div className="mt-1 text-lg font-semibold">
                      {idea.symbol}
                      <span className="ml-2 text-sm muted">{idea.name || ""}</span>
                    </div>
                    <div className="mt-2 text-sm text-textSecondary">
                      {idea.summary || "Model-ranked opportunity ready for review."}
                    </div>
                  </div>
                  <div className="rounded-full bg-positive px-3 py-1 text-lg font-bold text-black">
                    {numericScore.toFixed(1)}
                  </div>
                </div>
                <div className="mt-3 text-sm text-textSecondary">
                  Confidence: {idea.confidence}
                </div>
                <div className="mt-4">
                  <Link
                    href={`/stocks/${encodeURIComponent(idea.symbol)}`}
                    className="secondary-cta"
                  >
                    See Full Analysis
                  </Link>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {alerts.length > 0 ? (
        <Card>
          <div className="flex items-start gap-3">
            <div className="text-2xl">Alert</div>
            <div>
              <div className="text-sm text-white/60">Risk Alert</div>
              <div className="mt-1 text-base font-semibold">
                {alerts.length} alert(s) need review
              </div>
              <div className="mt-2 text-sm text-textSecondary">
                {alerts[0].message || alerts[0].reason || "Latest snapshot flagged a risk change."}
              </div>
            </div>
          </div>
        </Card>
      ) : null}

      <div className="flex flex-wrap gap-3">
        <Link href="/alpha-lab" className="secondary-cta">
          View Alpha Lab
        </Link>
        <Link href="/stocks" className="secondary-cta">
          Check Top Stocks
        </Link>
        <form method="post" action="/api/run-alpha" className="m-0">
          <button type="submit" className="primary-cta">
            Refresh Research Mode
          </button>
        </form>
      </div>
    </div>
  );
}
