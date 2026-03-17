import { NextResponse } from 'next/server'

export async function GET() {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
  const res = await fetch(`${apiUrl}/alpha/strategies`)
  const body = await res.text()
  return new NextResponse(body, { status: res.status, headers: { 'content-type': 'application/json' } })
}
