import { NextResponse } from "next/server";
import { getWatchlistsLocal } from "@/lib/local-data";

export async function GET() {
  return NextResponse.json(await getWatchlistsLocal());
}
