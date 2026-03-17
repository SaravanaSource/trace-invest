"use client"
import React from 'react'
import Link from 'next/link'

export default function HeaderBar({ title, generatedAt, nextUpdateText }: { title:string, generatedAt?:string|null, nextUpdateText?:string }){
  const lastUpdatedText = generatedAt ? new Date(generatedAt).toLocaleString() : 'N/A'
  return (
    <div className="flex items-baseline justify-between mb-8">
      <div>
        <h1 className="text-2xl font-semibold">{title}</h1>
        <div className="text-sm muted mt-1">Next update in {nextUpdateText || 'Weekly'} • Last updated: {lastUpdatedText}</div>
      </div>
      <div className="flex items-center gap-3">
        <Link href="/alpha-lab/signals" className="text-sm text-muted hover:text-textPrimary">Signals</Link>
        <Link href="/alpha-lab/strategies" className="text-sm text-muted hover:text-textPrimary">Strategies</Link>
        <Link href="/alpha-lab/backtests" className="text-sm text-muted hover:text-textPrimary">Backtests</Link>
        <button className="ml-2 bg-positive text-black rounded-md px-3 py-1.5 shadow-sm hover:opacity-95 transition">Run Analysis</button>
      </div>
    </div>
  )
}
