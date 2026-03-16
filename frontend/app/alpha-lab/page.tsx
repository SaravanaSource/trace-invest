"use client"
import React, {useEffect, useState} from 'react'
import Link from 'next/link'

export default function AlphaLabPage(){
  const [top, setTop] = useState<any>(null)
  useEffect(()=>{
    fetch('http://localhost:8000/alpha/top')
      .then(r=>r.json()).then(j=>setTop(j)).catch(()=>setTop({top:[]}))
  },[])

  return (
    <div style={{padding:20}}>
      <h1>Alpha Lab</h1>
      <nav style={{marginBottom:16}}>
        <Link href="/alpha-lab/signals">Signals</Link> |{' '}
        <Link href="/alpha-lab/strategies">Strategies</Link> |{' '}
        <Link href="/alpha-lab/backtests">Backtests</Link> |{' '}
        <Link href="/alpha-lab/rankings">Rankings</Link>
      </nav>
      <section style={{marginTop:12}}>
        <h2>Top Strategies</h2>
        {top?.top?.length ? (
          <ol>
            {top.top.map((s:any)=> <li key={s.strategy}>{s.strategy} — {s.alpha_score}</li>)}
          </ol>
        ) : (
          <div>No top strategies yet (run pipeline)</div>
        )}
      </section>
    </div>
  )
}
