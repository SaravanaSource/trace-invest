"use client"
import React, {useState} from 'react'

export default function Card({card, index}:{card:any, index:number}) {
  const [hover, setHover] = useState(false)
  const [open, setOpen] = useState(false)
  const numericScore = Number(card.score ?? card.result?.score ?? 0)
  const showNumericScore = numericScore > 0
  const confidence = (card.confidence || 'Medium') as string
  const risk = card.riskLevel || 'Moderate'
  const isTop = index === 0

  const scoreColor = numericScore >= 8 ? 'bg-positive text-black' : numericScore >= 6 ? 'bg-warning text-black' : 'bg-negative text-white'

  const rawSummary = card.what || card.summary || (card.reasons && card.reasons.length ? card.reasons[0] : 'Model-driven idea.')
  const mapSignalName = (s:string)=>{
    if(!s) return s
    const n = s.toLowerCase()
    if(n.includes('volatility_drop')) return 'Stabilizing price movement'
    if(n.includes('momentum_breakout')) return 'Strong upward momentum'
    return s.replace(/_/g,' ').replace(/\b\w/g, c=>c.toUpperCase())
  }
  const summary = mapSignalName(rawSummary)

  const reliabilityLabel = card.unreliable || card.reliability === 'low' ? 'Under Evaluation' : 'Emerging Signal'

  const renderConfidence = (c:string)=>{
    const k = (c||'Medium').toLowerCase()
    if(k.includes('high')) return (<div className="text-sm font-semibold text-white"><span className="text-amber-400">●●●</span> <span className="ml-2 muted">High</span></div>)
    if(k.includes('low')) return (<div className="text-sm font-semibold text-white"><span className="text-amber-400">●○○</span> <span className="ml-2 muted">Low</span></div>)
    return (<div className="text-sm font-semibold text-white"><span className="text-amber-400">●●○</span> <span className="ml-2 muted">Medium</span></div>)
  }

  return (
    <article
      onMouseEnter={()=>setHover(true)}
      onMouseLeave={()=>setHover(false)}
      onClick={()=>setOpen(!open)}
      role="button"
      className={`card-bg border border-borderSoft rounded-xl p-6 transition-transform duration-200 ${hover ? 'translate-y-[-6px] shadow-xl' : ''} ${isTop ? 'ring-4 ring-yellow-400/20 scale-105' : ''}`}
    >
      <div className="flex justify-between items-start">
        <div className="max-w-[65%]">
          <div className="text-xs muted">#{index+1}</div>
          <div className="flex items-baseline gap-3">
            <div className="text-xl md:text-2xl font-semibold">{card.symbol}</div>
            <div className="text-sm muted">{card.name || ''}</div>
            {isTop && <div className="ml-3 inline-flex items-center gap-2 px-2 py-1 rounded-full bg-yellow-500/10 text-sm font-semibold">🔥 Top Pick Today</div>}
          </div>
          <div className="text-lg md:text-xl font-bold mt-3 leading-snug">{summary}</div>
          <div className="text-sm text-white/70 mt-2">{card.note || ''}</div>
        </div>

        <div className="text-right">
          {showNumericScore ? (
            <div className={`inline-flex items-center justify-center px-3 py-1 rounded-full font-bold text-lg ${scoreColor}`}>{numericScore.toFixed(1)}</div>
          ) : (
            <div className="inline-flex items-center justify-center px-3 py-1 rounded-full font-semibold text-sm bg-surface text-white">{reliabilityLabel}</div>
          )}

          <div className="text-xs muted mt-2">{renderConfidence(confidence)} <div className="mt-1 muted">• {risk}</div></div>
        </div>
      </div>

      <div className="mt-5">
        <div className="text-sm font-medium">Why it matters</div>
        <div className="text-sm text-textSecondary mt-2">This stock is showing early signs of potential movement and is worth monitoring.</div>
        <ul className="list-disc ml-5 mt-2 text-sm space-y-1">
          {(card.reasons || []).slice(0,3).map((r:any,i:number)=>(
            <li key={i}>{r}</li>
          ))}
        </ul>
      </div>

      <div className="mt-4 p-4 bg-white/2 rounded-md">
        <div className="text-sm font-semibold">What to do</div>
        <div className="text-sm text-textSecondary mt-1">Watch closely — potential opportunity forming.</div>
        <div className="mt-3 flex gap-3">
          <button onClick={(e)=>{e.stopPropagation(); console.log('view', card.symbol)}} className="px-4 py-2 rounded-md bg-transparent border border-white/6 text-textPrimary hover:opacity-90">See Full Analysis →</button>
          <button onClick={(e)=>{e.stopPropagation(); console.log('watch', card.symbol)}} className="px-4 py-2 rounded-md bg-positive text-black font-semibold hover:opacity-95">Add to Watchlist</button>
        </div>
      </div>

      <div className="mt-3 text-xs muted">Horizon: 2–8 weeks • Confidence: {confidence} • Risk: {risk}</div>

      {open && <div className="mt-3 text-sm text-textSecondary">Expanded details: more context, links to backtests and source data.</div>}
    </article>
  )
}
