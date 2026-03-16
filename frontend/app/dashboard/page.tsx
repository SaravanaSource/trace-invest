import { Card } from "@/components/ui/Card";
import { Stat } from "@/components/ui/Stat";
import { getMarketSummary } from "@/lib/api";

type MarketSummary = {
  total_stocks: number;
  by_decision_zone: Record<string, number>;
  by_overall_risk: Record<string, number>;
  upgrades?: number;
  downgrades?: number;
  market_tone?: string;
};

function formatMap(map: Record<string, number> | undefined) {
  if (!map || Object.keys(map).length === 0) {
    return <div className="text-white/60">No data</div>;
  }

  return (
    <ul className="space-y-1 text-white/80">
      {Object.entries(map).map(([key, value]) => (
        <li key={key} className="flex items-center justify-between">
          <span>{key}</span>
          <span className="font-semibold text-white">{value}</span>
        </li>
      ))}
    </ul>
  );
}

export default async function Dashboard() {
  let summary: MarketSummary | null = null;

  try {
    summary = await getMarketSummary();
  } catch (error) {
    console.error(error);
  }

  if (!summary) {
    return <div className="p-6 text-white/60">Failed to load market summary.</div>;
  }

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-3xl font-bold">Dashboard</h1>

      <div className="grid gap-4 md:grid-cols-4">
        <Stat label="Total Stocks" value={summary.total_stocks} />
        <Stat label="Upgrades" value={summary.upgrades ?? 0} tone="good" />
        <Stat label="Downgrades" value={summary.downgrades ?? 0} tone="bad" />
        <Stat label="Market Tone" value={summary.market_tone || "UNKNOWN"} />
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <div className="text-sm text-white/60 mb-3">Decision Zones</div>
          {formatMap(summary.by_decision_zone)}
        </Card>
        <Card>
          <div className="text-sm text-white/60 mb-3">Risk Bands</div>
          {formatMap(summary.by_overall_risk)}
        </Card>
      </div>
    </div>
  );
}
