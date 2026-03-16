"use client"
import React, {useEffect, useState} from 'react'

export default function SignalsPage(){
  const [data,setData]=useState<any>(null)
  useEffect(()=>{
    fetch('http://localhost:8000/alpha/signals')
      .then(r=>r.json()).then(j=>setData(j)).catch(()=>setData({signals:[]}))
  },[])

  return (
    <div style={{padding:20}}>
      <h1>Signals</h1>
      {data?.signals?.length ? (
        <table style={{width:'100%',borderCollapse:'collapse'}}>
          <thead><tr><th style={{textAlign:'left'}}>Signal</th><th>Symbol</th><th>Strength</th><th>Explanation</th></tr></thead>
          <tbody>
            {data.signals.map((s:any, i:number)=>(
              <tr key={i} style={{borderTop:'1px solid #eee'}}>
                <td>{s.signal_name}</td>
                <td>{s.symbol}</td>
                <td>{s.signal_strength}</td>
                <td>{s.explanation}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <div>No signals found</div>
      )}
    </div>
  )
}
