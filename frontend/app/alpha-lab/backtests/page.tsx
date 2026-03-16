"use client"
import React, {useEffect, useState} from 'react'

export default function BacktestsPage(){
  const [monitor,setMonitor]=useState<any>(null)
  useEffect(()=>{
    fetch('http://localhost:8000/alpha/monitoring')
      .then(r=>r.json()).then(j=>setMonitor(j)).catch(()=>setMonitor({monitoring:[]}))
  },[])

  return (
    <div style={{padding:20}}>
      <h1>Backtests / Monitoring</h1>
      {monitor?.monitoring?.length ? (
        <div>
          {monitor.monitoring.map((m:any,i:number)=>(
            <div key={i} style={{border:'1px solid #eee',padding:8,marginBottom:8}}>
              <strong>{m.strategy}</strong>
              <div>Last monthly return: {m.monthly_return_last}</div>
              <div>Rolling Sharpe (12m): {m.rolling_sharpe_12m}</div>
            </div>
          ))}
        </div>
      ) : (
        <div>No monitoring data yet</div>
      )}
    </div>
  )
}
