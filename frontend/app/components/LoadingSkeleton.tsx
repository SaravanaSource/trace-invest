"use client"
import React from 'react'
import { COLORS, SPACE } from '../styles/theme'

export default function LoadingSkeleton({count=3}:{count?:number}){
  return (
    <div style={{display:'grid', gap:12}}>
      <style>{`
        @keyframes pulseSkeleton { 0% { opacity: 1 } 50% { opacity: 0.6 } 100% { opacity: 1 } }
      `}</style>
      {Array.from({length:count}).map((_,i)=> (
        <div key={i} className="card-bg border border-borderSoft rounded-xl p-4">
          <div className="h-3 w-2/5 bg-white/6 rounded animate-pulse mb-3"></div>
          <div className="h-2 w-1/3 bg-white/5 rounded mb-2 animate-pulse"></div>
          <div className="h-2 w-4/5 bg-white/4 rounded animate-pulse"></div>
        </div>
      ))}
    </div>
  )
}
