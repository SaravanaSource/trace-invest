import { NextResponse } from "next/server";
import { getAlphaSignalsLocal } from "@/lib/local-data";

export async function GET() {
  return NextResponse.json(await getAlphaSignalsLocal());
}
