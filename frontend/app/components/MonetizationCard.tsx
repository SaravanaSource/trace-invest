"use client"
import React from 'react'

export default function MonetizationCard(){
  return (
    <div className="rounded-xl p-4" style={{background: 'linear-gradient(90deg, rgba(34,197,94,0.06), rgba(255,255,255,0.03))', border: '1px solid rgba(255,255,255,0.03)'}}>
      <div className="font-semibold mb-2">Premium — Unlock full analysis</div>
      <div className="text-sm text-textSecondary mb-3">Subscribe to access full backtests, model explanations, and personalized alerts.</div>
      <button className="w-full bg-positive text-black py-2 rounded-md font-semibold hover:opacity-95 transition">Upgrade</button>
      <div className="text-xs muted mt-3">Not investment advice. Past performance is not indicative of future results.</div>
    </div>
  )
}
