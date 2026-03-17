"use client"
import React, {useEffect, useState} from 'react'
import Link from 'next/link'
import HeaderBar from '../components/HeaderBar'
import Card from '../components/Card'
import ScoreGuide from '../components/ScoreGuide'
import MonetizationCard from '../components/MonetizationCard'
import EmptyState from '../components/EmptyState'
import LoadingSkeleton from '../components/LoadingSkeleton'

type Ranking = { strategy: string; alpha_score: number; CAGR?: number; max_drawdown?: number; volatility?: number; sharpe?: number }
type Strategy = { strategy_name: string; positions: { symbol: string; weight: number }[] }
type Signal = { signal_name: string; symbol: string; explanation: string }

export default function AlphaLabPage(){
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
  console.log('API URL:', apiUrl)
  const [rankings, setRankings] = useState<Ranking[]>([])
  const [strategies, setStrategies] = useState<Strategy[]>([])
  const [signals, setSignals] = useState<Signal[]>([])
  const [generatedAt, setGeneratedAt] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(()=>{
    console.log('Fetching alpha data from', apiUrl)
    // fetch rankings, strategies and signals in parallel
    Promise.all([
      // Use local API proxy to avoid CORS issues: Next.js server will forward to backend
      fetch(`/api/alpha/rankings`).then(async r=>{ if(!r.ok){ const t = await r.text(); throw new Error(`rankings fetch failed: ${r.status} ${t}`)}; return r.json() }),
      fetch(`/api/alpha/strategies`).then(async r=>{ if(!r.ok){ const t = await r.text(); throw new Error(`strategies fetch failed: ${r.status} ${t}`)}; return r.json() }),
      fetch(`/api/alpha/signals`).then(async r=>{ if(!r.ok){ const t = await r.text(); throw new Error(`signals fetch failed: ${r.status} ${t}`)}; return r.json() }),
    ]).then(([ranks, strs, sigs])=>{
      setRankings(ranks.rankings || [])
      setStrategies(strs.strategies || [])
      setSignals(sigs.signals || [])
      // preserve generated_at for freshness display
      setGeneratedAt(ranks.generated_at || strs.generated_at || sigs.generated_at || null)
    }).catch(err=>{
      console.error('Alpha API error', err)
      setError(err?.message || err?.error || err?.detail || 'Failed to load data. Run pipeline.')
    })
  },[])

  // helper: map strategy name -> strategy object
  const stratMap: Record<string, Strategy> = {}
  strategies.forEach(s=>{ (stratMap as any)[s.strategy_name] = s })

  // Build aggregated, de-duplicated cards per stock (one stock => one score)
  // Friendly symbol display names for demo data
  const SYMBOL_NAMES: Record<string,string> = { AAA: 'Demo Stock A (Tech)', BBB: 'Demo Stock B (Finance)', CCC: 'Demo Stock C (Energy)' }

  // Build aggregated list of symbols from rankings and strategies
  const symbolBest: Record<string,{strategy?:string,alpha?:number}> = {}
  for(const r of rankings){
    const stratDef = strategies.find(s=>s.strategy_name === r.strategy)
    if(!stratDef || !Array.isArray(stratDef.positions)) continue
    for(const p of stratDef.positions){
      const sym = p.symbol
      if(!sym) continue
      if(!(sym in symbolBest)){
        symbolBest[sym] = { strategy: r.strategy, alpha: r.alpha_score }
      }
    }
  }

  const symbolList = Object.entries(symbolBest).map(([sym, v])=> ({ symbol: sym, meta: v }))
    .slice(0, 50)

  const topN = 5

  // Plain-language mapping for signals
  const SIGNAL_PHRASES: Record<string,string> = {
    momentum_breakout: 'Strong recent upward trend',
    volatility_drop: 'Price movements have settled recently',
    earnings_acceleration: 'Earnings improving over recent quarters',
    insider_accumulation: 'Insider buying activity detected',
  }

  // Compute cards with simplified, trustable presentation
  const total = Math.max(1, symbolList.length)
  const cards = symbolList.slice(0, topN).map((item, idx)=>{
    const sym = item.symbol
    const displayName = SYMBOL_NAMES[sym] || sym
    const relatedSignalsFull = signals.filter(s=>s.symbol === sym)
    const relatedSignals = relatedSignalsFull.map(s=> SIGNAL_PHRASES[s.signal_name] || s.explanation ).filter(Boolean)

    // base percentile score (0..1) where 1 is top
    const percentile = total <= 1 ? 1 : (1 - (idx / (total - 1)))
    let score = Math.round(((percentile * 9) + 1) * 10) / 10 // 1.0..10.0

    // small boost for more signals (up to +0.5)
    const boost = Math.min(relatedSignals.length, 3) / 3 * 0.5
    score = Math.min(10, Math.round((score + boost) * 10) / 10)

    // verdict labels (legal-safe)
    const verdict = score >= 8 ? 'Strong Opportunity' : score >=5 ? 'Favorable' : 'Watch / Higher Risk'

    // confidence badge: High (>=3 signals) | Medium (2) | Low (<=1)
    const confidence = relatedSignals.length >=3 ? 'High' : relatedSignals.length ===2 ? 'Medium' : 'Low'

    // risk level: derive from available ranking metrics but do NOT show raw numbers
    // find a representative ranking entry for this symbol (first strategy that contains it)
    const repRank = rankings.find(r=>{
      const sdef = strategies.find(s=>s.strategy_name === r.strategy)
      return sdef && Array.isArray(sdef.positions) && sdef.positions.some(p=>p.symbol === sym)
    })

    let riskLevel = 'Medium'
    if(repRank){
      const md = (repRank.max_drawdown ?? null)
      const vol = (repRank.volatility ?? null)
      const sharpe = (repRank.sharpe ?? null)
      const suspicious = (sharpe && sharpe > 10) || (md === 0 && vol === 0)
      if(suspicious){
        riskLevel = 'Medium'
      } else {
        if(md !== null && md <= -0.5) riskLevel = 'High'
        else if(vol !== null && vol >= 0.35) riskLevel = 'High'
        else if(md !== null && md <= -0.25) riskLevel = 'Medium'
        else riskLevel = 'Low'
      }
    }

    const note = 'Based on model-driven analysis. Not financial advice.'

    return {
      stock: sym,
      displayName,
      score,
      verdict,
      why: relatedSignals.slice(0,3),
      riskLevel,
      confidence,
      note,
    }
  })

  // freshness / update timing
  const lastUpdatedText = generatedAt ? new Date(generatedAt).toISOString() : 'N/A'
  let nextUpdateText = 'Weekly'
  if(generatedAt){
    const gen = new Date(generatedAt)
    const next = new Date(gen.getTime() + 7*24*60*60*1000)
    const now = new Date()
    const ms = next.getTime() - now.getTime()
    const days = Math.ceil(ms / (24*60*60*1000))
    nextUpdateText = days > 0 ? `${days} day${days>1? 's':''}` : 'Today'
  }
  // normalize cards for Card component
  const normalizedCards = cards.map(c=> ({
    symbol: c.stock,
    name: c.displayName,
    what: c.verdict,
    score: c.score,
    confidence: c.confidence,
    riskLevel: c.riskLevel,
    reasons: c.why
  }))

  return (
    <div className="p-8">
      <HeaderBar title="Alpha Lab — curated ideas" generatedAt={generatedAt} nextUpdateText={nextUpdateText} />

      <div className="grid grid-cols-[1fr_320px] gap-8 mt-4">
        <div>
          {error ? (
            <div className="p-3 rounded-md bg-gradient-to-r from-amber-50 to-white/5 border border-white/5 text-warning">No insights available yet. {String(error)}</div>
          ) : null}

          {(!normalizedCards || normalizedCards.length === 0) ? <EmptyState /> : (
            <div className="grid gap-4">
              {normalizedCards.map((c,i)=> (
                <Card key={c.symbol} card={c} index={i} />
              ))}
            </div>
          )}
        </div>

        <aside className="flex flex-col gap-4">
          <ScoreGuide />
          <MonetizationCard />
        </aside>
      </div>
    </div>
  )
}
