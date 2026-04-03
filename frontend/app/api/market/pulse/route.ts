import { NextResponse } from "next/server";
import { getMarketPulseLocal } from "@/lib/local-data";

export async function GET() {
  return NextResponse.json(await getMarketPulseLocal());
}
