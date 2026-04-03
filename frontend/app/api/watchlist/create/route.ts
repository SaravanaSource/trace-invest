import { NextResponse } from "next/server";
import { createWatchlistLocal } from "@/lib/local-data";

export async function POST(request: Request) {
  const payload = await request.json();
  return NextResponse.json(await createWatchlistLocal(payload));
}
