import { NextResponse } from 'next/server'

export async function POST(req: Request) {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
  const body = await req.text()
  const res = await fetch(`${apiUrl}/alpha/run`, { method: 'POST', body, headers: { 'content-type': 'application/json' } })
  const text = await res.text()
  return new NextResponse(text, { status: res.status, headers: { 'content-type': 'application/json' } })
}
