import Link from "next/link";
import { Card } from "@/components/ui/Card";
import { getAlerts, getMarketPulse } from "@/lib/api";
import type { MarketPulse, ValueCandidate } from "@/lib/local-data";

function scoreTone(score: number) {
  if (score >= 80) {
    return "Prime Setup";
  }
  if (score >= 65) {
    return "Strong Watch";
  }
  if (score >= 50) {
    return "Selective";
  }
  return "Needs Patience";
}

function formatPercent(value: number | null) {
  if (value === null) {
    return "N/A";
  }
  const prefix = value > 0 ? "+" : "";
  return `${prefix}${value.toFixed(1)}%`;
}

function metricLabel(candidate: ValueCandidate) {
  return [
    `${candidate.signal_count} active signals`,
    `${candidate.strategy_count} supporting strategies`,
    `confidence ${candidate.confidence}`,
  ].join(" | ");
}

export default async function Dashboard() {
  const pulse: MarketPulse = await getMarketPulse();
  const alerts = await getAlerts();
  const pinned = pulse.pinned_stock;
  const runnerUps = pulse.candidates.slice(1, 5);

  return (
    <div className="max-w-6xl space-y-6 p-6">
      <Card>
        <div className="hero-panel overflow-hidden rounded-2xl border border-borderSoft p-8">
          <div className="flex flex-col gap-8 lg:flex-row lg:items-end lg:justify-between">
            <div className="max-w-3xl space-y-4">
              <div className="text-xs uppercase tracking-[0.35em] text-white/55">
                Market Pulse
              </div>
              <h1 className="text-3xl font-extrabold leading-tight lg:text-5xl">
                {pulse.headline}
              </h1>
              <p className="max-w-2xl text-base leading-7 text-textSecondary">
                {pulse.summary}
              </p>
              <div className="inline-flex rounded-full border border-emerald-300/20 bg-emerald-300/10 px-4 py-2 text-sm text-emerald-100">
                {pulse.action}
              </div>
            </div>

            <div className="grid min-w-[280px] gap-3 sm:grid-cols-3 lg:w-[360px] lg:grid-cols-1">
              <div className="rounded-2xl border border-border bg-white/5 p-4">
                <div className="text-xs uppercase tracking-[0.25em] text-white/45">Tone</div>
                <div className="mt-2 text-2xl font-bold">{pulse.tone}</div>
              </div>
              <div className="rounded-2xl border border-border bg-white/5 p-4">
                <div className="text-xs uppercase tracking-[0.25em] text-white/45">Pinned Stock</div>
                <div className="mt-2 text-2xl font-bold">{pinned?.symbol || "None"}</div>
              </div>
              <div className="rounded-2xl border border-border bg-white/5 p-4">
                <div className="text-xs uppercase tracking-[0.25em] text-white/45">As Of</div>
                <div className="mt-2 text-lg font-bold">{pulse.as_of || "No snapshot"}</div>
              </div>
            </div>
          </div>
        </div>
      </Card>

      <div className="grid gap-4 lg:grid-cols-[1.45fr_0.95fr]">
        <Card>
          <div className="flex items-start justify-between gap-4">
            <div>
              <div className="text-xs uppercase tracking-[0.28em] text-white/50">
                Best Value Candidate
              </div>
              <h2 className="mt-2 text-2xl font-bold">
                {pinned ? `${pinned.symbol} is the stock to start with.` : "No stock is pinned yet."}
              </h2>
              <div className="mt-3 max-w-2xl text-sm leading-7 text-textSecondary">
                {pinned?.narrative ||
                  "Once more local market breadth is available, the dashboard will pin the best current setup here."}
              </div>
            </div>
            {pinned ? (
              <div className="rounded-2xl bg-positive px-4 py-3 text-right text-black shadow-lg shadow-emerald-500/20">
                <div className="text-xs font-bold uppercase tracking-[0.2em]">Opportunity Score</div>
                <div className="mt-1 text-3xl font-extrabold">{pinned.score.toFixed(1)}</div>
                <div className="text-xs font-semibold">{scoreTone(pinned.score)}</div>
              </div>
            ) : null}
          </div>

          {pinned ? (
            <>
              <div className="mt-6 grid gap-3 md:grid-cols-4">
                <div className="rounded-2xl border border-border bg-white/4 p-4">
                  <div className="text-xs uppercase tracking-[0.2em] text-white/45">Alpha Strength</div>
                  <div className="mt-2 text-2xl font-bold">{pinned.alpha_score.toFixed(0)}</div>
                </div>
                <div className="rounded-2xl border border-border bg-white/4 p-4">
                  <div className="text-xs uppercase tracking-[0.2em] text-white/45">Price Move</div>
                  <div className="mt-2 text-2xl font-bold">{formatPercent(pinned.price_change_pct)}</div>
                </div>
                <div className="rounded-2xl border border-border bg-white/4 p-4">
                  <div className="text-xs uppercase tracking-[0.2em] text-white/45">Valuation View</div>
                  <div className="mt-2 text-2xl font-bold">{pinned.valuation_view}</div>
                </div>
                <div className="rounded-2xl border border-border bg-white/4 p-4">
                  <div className="text-xs uppercase tracking-[0.2em] text-white/45">Risk</div>
                  <div className="mt-2 text-2xl font-bold">{pinned.risk_level}</div>
                </div>
              </div>

              <div className="mt-6 grid gap-4 md:grid-cols-2">
                <div className="rounded-2xl border border-emerald-400/15 bg-emerald-400/5 p-5">
                  <div className="text-xs uppercase tracking-[0.22em] text-emerald-100/70">
                    Why It Looks Valuable
                  </div>
                  <div className="mt-3 space-y-3 text-sm leading-7 text-emerald-50">
                    {pinned.reasons.map((reason) => (
                      <div key={reason}>{reason}</div>
                    ))}
                  </div>
                </div>

                <div className="rounded-2xl border border-amber-300/15 bg-amber-300/5 p-5">
                  <div className="text-xs uppercase tracking-[0.22em] text-amber-100/70">
                    What Could Go Wrong
                  </div>
                  <div className="mt-3 space-y-3 text-sm leading-7 text-amber-50">
                    {pinned.risks.map((risk) => (
                      <div key={risk}>{risk}</div>
                    ))}
                  </div>
                </div>
              </div>

              <div className="mt-6 flex flex-wrap gap-3">
                <Link
                  href={`/stocks/${encodeURIComponent(pinned.symbol)}`}
                  className="primary-cta"
                >
                  Open {pinned.symbol} Analysis
                </Link>
                <Link
                  href={`/stocks/${encodeURIComponent(pinned.symbol)}/reasoning`}
                  className="secondary-cta"
                >
                  Read Reasoning
                </Link>
              </div>
            </>
          ) : null}
        </Card>

        <div className="space-y-4">
          <Card>
            <div className="text-xs uppercase tracking-[0.28em] text-white/50">What Is Happening Now</div>
            <div className="mt-4 space-y-4 text-sm leading-7 text-textSecondary">
              <div>
                <span className="font-semibold text-text">Breadth:</span> {pulse.breadth_view}
              </div>
              <div>
                <span className="font-semibold text-text">Risk Pressure:</span> {pulse.risk_view}
              </div>
              <div>
                <span className="font-semibold text-text">Setup Leadership:</span> {pulse.leadership_view}
              </div>
            </div>
          </Card>

          <Card>
            <div className="text-xs uppercase tracking-[0.28em] text-white/50">Evidence Stack</div>
            <div className="mt-4 space-y-3 text-sm leading-7 text-textSecondary">
              {pulse.evidence.map((item) => (
                <div key={item}>{item}</div>
              ))}
            </div>
          </Card>

          {alerts.length > 0 ? (
            <Card>
              <div className="text-xs uppercase tracking-[0.28em] text-white/50">Risk Alert</div>
              <div className="mt-3 text-lg font-semibold">
                {alerts.length} alert{alerts.length === 1 ? "" : "s"} need review
              </div>
              <div className="mt-3 text-sm leading-7 text-textSecondary">
                {alerts[0].message || alerts[0].reason || "Latest snapshot flagged a risk change."}
              </div>
            </Card>
          ) : null}
        </div>
      </div>

      <Card>
        <div className="flex items-center justify-between gap-4">
          <div>
            <div className="text-xs uppercase tracking-[0.28em] text-white/50">Next Best Names</div>
            <h2 className="mt-2 text-2xl font-bold">Runner-up valuable stocks</h2>
          </div>
          <Link href="/stocks" className="secondary-cta">
            Explore All Stocks
          </Link>
        </div>

        <div className="mt-5 grid gap-4 md:grid-cols-3">
          {runnerUps.map((candidate) => (
            <div key={candidate.symbol} className="rounded-2xl border border-border bg-white/4 p-5">
              <div className="flex items-start justify-between gap-3">
                <div>
                  <div className="text-lg font-bold">{candidate.symbol}</div>
                  <div className="mt-1 text-xs uppercase tracking-[0.22em] text-white/45">
                    {scoreTone(candidate.score)}
                  </div>
                </div>
                <div className="rounded-full border border-white/10 px-3 py-1 text-sm font-semibold text-white/80">
                  {candidate.score.toFixed(1)}
                </div>
              </div>

              <div className="mt-4 text-sm leading-7 text-textSecondary">
                {candidate.reasons[0]}
              </div>

              <div className="mt-4 text-xs uppercase tracking-[0.18em] text-white/45">
                {metricLabel(candidate)}
              </div>

              <div className="mt-4 flex flex-wrap gap-2 text-xs">
                <span className="rounded-full bg-white/6 px-3 py-1 text-white/70">
                  risk {candidate.risk_level}
                </span>
                <span className="rounded-full bg-white/6 px-3 py-1 text-white/70">
                  valuation {candidate.valuation_view}
                </span>
                <span className="rounded-full bg-white/6 px-3 py-1 text-white/70">
                  recent {formatPercent(candidate.recent_change_pct)}
                </span>
              </div>

              <div className="mt-5">
                <Link
                  href={`/stocks/${encodeURIComponent(candidate.symbol)}`}
                  className="secondary-cta"
                >
                  Review {candidate.symbol}
                </Link>
              </div>
            </div>
          ))}
        </div>
      </Card>

      <div className="flex flex-wrap gap-3">
        <Link href="/alpha-lab" className="secondary-cta">
          View Alpha Lab
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
