"use client"
import React from 'react'

export default function EmptyState({message}:{message?:string}){
  return (
    <div className="py-12 text-center">
      <div className="text-lg font-semibold mb-2">No ideas yet</div>
      <div className="text-sm text-textSecondary">{message || 'We couldn\'t find signals for the current universe. Try widening the universe or re-running analysis.'}</div>
    </div>
  )
}
