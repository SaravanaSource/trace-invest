import { NextResponse } from "next/server";
import { getPortfolioLocal } from "@/lib/local-data";

export async function GET() {
  return NextResponse.json(await getPortfolioLocal());
}
