import { NextResponse } from "next/server";
import { getAlphaRankingsLocal } from "@/lib/local-data";

export async function GET() {
  return NextResponse.json(await getAlphaRankingsLocal());
}
