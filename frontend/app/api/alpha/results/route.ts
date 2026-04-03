import { NextResponse } from "next/server";
import { getAlphaResultsLocal } from "@/lib/local-data";

export async function GET() {
  return NextResponse.json(await getAlphaResultsLocal());
}
