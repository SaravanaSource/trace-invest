"use client"
import React, {useEffect, useState} from 'react'

export default function StrategiesPage(){
  const [data,setData]=useState<any>(null)
  useEffect(()=>{
    fetch('http://localhost:8000/alpha/strategies')
      .then(r=>r.json()).then(j=>setData(j)).catch(()=>setData({strategies:[]}))
  },[])

  return (
    <div style={{padding:20}}>
      <h1>Generated Strategies</h1>
      {data?.strategies?.length ? (
        <div>
          {data.strategies.map((s:any, i:number)=>(
            <div key={i} style={{border:'1px solid #eee',padding:8,marginBottom:8}}>
              <strong>{s.strategy_name}</strong>
              <div>Rules: <pre style={{whiteSpace:'pre-wrap'}}>{JSON.stringify(s.rules,null,2)}</pre></div>
            </div>
          ))}
        </div>
      ) : (
        <div>No generated strategies yet</div>
      )}
    </div>
  )
}
