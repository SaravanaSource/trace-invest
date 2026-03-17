import { Card } from "@/components/ui/Card";
import { Stat } from "@/components/ui/Stat";
import { getMarketSummary, getAlphaResults, getAlerts, runAlphaNow } from "@/lib/api";

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
  let alpha: any[] = []
  let alerts: any[] = []

  try {
    summary = await getMarketSummary();
    // Fetch alpha results at request time to ensure fresh top ideas
    try {
      const apiBase = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const r = await fetch(`${apiBase}/alpha/results`, { cache: 'no-store' })
      const raw = await r.json().catch(()=>null)
      const list = Array.isArray(raw) ? raw : (raw?.results || raw?.strategies || [])
      alpha = (list || []).map((a:any)=>{
        const pos = a.result?.positions?.[0] || a.positions?.[0] || {}
        return {
          symbol: pos.symbol,
          name: pos.name || '',
          summary: a.result?.strategy || a.strategy || '',
          score: a.score || a.result?.score || 0,
          confidence: a.confidence || 'Medium',
          action: 'Consider tracking for entry'
        }
      })
    } catch(e) {
      alpha = []
    }
    alerts = await getAlerts().catch(()=>[])
  } catch (error) {
    console.error(error);
  }

  if (!summary) {
    return <div className="p-6 text-white/60">Failed to load market summary.</div>;
  }

  // Derive readable market tone
  const tone = (summary.market_tone || 'UNKNOWN').toUpperCase()
  const toneExplainer = tone === 'CAUTIOUS'
    ? 'Market showing uncertainty — avoid aggressive positions.'
    : tone === 'BULLISH'
      ? 'Market showing strength — prioritize high-conviction ideas.'
      : tone === 'BEARISH'
        ? 'Market trending lower — favor risk management and cash.'
        : 'Mixed signals — focus on high-confidence opportunities.'

  return (
    <div className="p-6 space-y-6 max-w-5xl">
      <h1 className="text-3xl font-bold">Daily Control Center</h1>
      <div className="text-sm text-white/70">AI-powered signals updated weekly</div>

      {/* Top: Today's Insight */}
      <div className="grid gap-4 md:grid-cols-3">
        <div className="md:col-span-2">
          <Card>
            <div className="flex items-start gap-4">
            <div className="text-4xl">📊</div>
            <div>
              <div className="text-sm text-white/60">Today’s Market Insight</div>
              <div className="text-2xl font-bold mt-2">{tone}</div>
              <div className="text-sm text-textSecondary mt-2">{toneExplainer}</div>
            </div>
          </div>
          </Card>
        </div>

        <Card>
          <div className="text-sm text-white/60">What you should do today</div>
          <ul className="mt-3 list-disc ml-5 space-y-2 text-sm">
            <li>Avoid aggressive buying; favor risk-managed entries.</li>
            <li>Focus on high-confidence stocks and clear edge.</li>
            <li>Monitor top opportunities and set alerts for entries.</li>
          </ul>
        </Card>
      </div>

      {/* Top opportunities (FOMO) */}
      <div>
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-semibold">Top opportunities right now</h2>
          <div className="text-sm text-white/60">Alpha Lab — top ranked ideas</div>
        </div>

        <div className="text-sm text-white/80 mt-1">Top opportunities right now</div>

        <div className="mt-4 space-y-4">
          {(alpha || []).slice(0,3).map((a:any, i:number)=>{
            const isTop = i === 0
            const mapSignalName = (s:string)=>{
              if(!s) return s
              const n = s.toLowerCase()
              if(n.includes('volatility_drop')) return 'Stabilizing price movement'
              if(n.includes('momentum_breakout')) return 'Strong upward momentum'
              return s.replace(/_/g,' ').replace(/\b\w/g, c=>c.toUpperCase())
            }
            const summary = mapSignalName(a.summary || a.what || (a.reasons && a.reasons[0]) || '')
            const numericScore = Number(a.score || 0)
            const scoreDisplay = numericScore > 0 ? numericScore.toFixed(1) : (a.unreliable || a.reliability==='low' ? 'Under Evaluation' : 'Emerging Signal')

            return (
              <div key={a.symbol} className={`card-bg border border-borderSoft rounded-xl p-6 transition-transform ${isTop ? 'ring-4 ring-yellow-400/20 scale-105' : ''}`}>
                <div className="flex justify-between items-start">
                  <div>
                    <div className="text-sm muted">#{i+1}</div>
                    <div className="text-lg font-semibold mt-1">{a.symbol} <span className="text-sm muted ml-2">{a.name || ''}</span></div>
                    <div className="text-sm mt-2 text-textSecondary">{summary}</div>
                  </div>

                  <div className="text-right">
                    {numericScore > 0 ? (
                      <div className={`inline-flex items-center justify-center px-3 py-1 rounded-full font-bold text-lg ${numericScore >= 8 ? 'bg-positive text-black' : numericScore >= 6 ? 'bg-warning text-black' : 'bg-negative text-white'}`}>{numericScore.toFixed(1)}</div>
                    ) : (
                      <div className="inline-flex items-center justify-center px-3 py-1 rounded-full font-semibold text-sm bg-surface text-white">{scoreDisplay}</div>
                    )}
                    <div className="text-xs muted mt-2">{a.confidence || 'Medium'}</div>
                  </div>
                </div>

                <div className="mt-3">
                  <div className="text-sm font-medium">Why it matters</div>
                  <div className="text-sm text-textSecondary mt-1">This stock is showing early signs of potential movement and is worth monitoring.</div>
                </div>

                <div className="mt-3 flex items-center justify-between">
                  <div className="text-sm text-textSecondary">Watch closely — potential opportunity forming</div>
                  <div className="flex gap-2">
                    <a href={`/stocks/${a.symbol}`} className="px-3 py-2 rounded-md bg-transparent border border-white/6 text-textPrimary">See Full Analysis →</a>
                  </div>
                </div>
              </div>
            )
          })}
          {(alpha || []).length === 0 && <div className="card-bg border border-borderSoft rounded-xl p-6">No top ideas available right now.</div>}
        </div>
      </div>

      {/* Risk Alert */}
      {alerts && alerts.length > 0 ? (
        <Card>
          <div className="flex items-start gap-3">
            <div className="text-2xl">⚠️</div>
            <div>
              <div className="text-sm text-white/60">Risk Alert</div>
              <div className="text-base font-semibold mt-1">{alerts.length} alert(s) — review immediately</div>
              <div className="text-sm text-textSecondary mt-2">{alerts[0].message || 'One or more stocks moved to higher risk.'}</div>
            </div>
          </div>
        </Card>
      ) : null}

      {/* Quick Actions */}
      <div className="flex gap-3">
        <a href="/alpha-lab" className="px-4 py-2 rounded-md bg-surface border border-border">View Alpha Lab</a>
        <a href="/stocks" className="px-4 py-2 rounded-md bg-surface border border-border">Check Top Stocks</a>
        <form method="post" action="/api/run-alpha" className="m-0">
          <button type="submit" className="px-4 py-2 rounded-md bg-positive text-black font-semibold">Run Analysis</button>
        </form>
      </div>
    </div>
  );
}
