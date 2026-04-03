import { NextResponse } from "next/server";
import { getAlphaStrategiesLocal } from "@/lib/local-data";

export async function GET() {
  return NextResponse.json(await getAlphaStrategiesLocal());
}
