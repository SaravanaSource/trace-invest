"use client"
import React from 'react'

export default function ScoreGuide(){
  return (
    <div className="card-bg border border-borderSoft rounded-xl p-4">
      <div className="font-semibold mb-2">Score guide</div>
      <div className="text-sm text-textSecondary">
        <div className="mb-1"><span className="font-medium">9–10</span> — Excellent</div>
        <div className="mb-1"><span className="font-medium">7–8</span> — Strong</div>
        <div className="mb-1"><span className="font-medium">5–6</span> — Moderate</div>
        <div className="mb-1"><span className="font-medium">1–4</span> — Weak</div>
      </div>
      <div className="text-xs muted mt-3">Information provided for educational purposes only and not financial advice.</div>
    </div>
  )
}
