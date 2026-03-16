"use client"
import React, {useEffect, useState} from 'react'

export default function RankingsPage(){
  const [data,setData]=useState<any>(null)
  useEffect(()=>{
    fetch('http://localhost:8000/alpha/rankings')
      .then(r=>r.json()).then(j=>setData(j)).catch(()=>setData({rankings:[]}))
  },[])

  return (
    <div style={{padding:20}}>
      <h1>Strategy Rankings</h1>
      {data?.rankings?.length ? (
        <table style={{width:'100%'}}>
          <thead><tr><th>Strategy</th><th>Alpha</th><th>CAGR</th><th>Sharpe</th></tr></thead>
          <tbody>
            {data.rankings.map((r:any,i:number)=>(
              <tr key={i} style={{borderTop:'1px solid #eee'}}>
                <td>{r.strategy}</td>
                <td>{r.alpha_score}</td>
                <td>{r.CAGR}</td>
                <td>{r.sharpe}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <div>No rankings available</div>
      )}
    </div>
  )
}
