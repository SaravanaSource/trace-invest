import { NextResponse } from "next/server";
import { getStockReasoningLocal } from "@/lib/local-data";

export async function GET(
  _request: Request,
  { params }: { params: Promise<{ symbol: string }> }
) {
  const { symbol } = await params;
  return NextResponse.json(await getStockReasoningLocal(symbol));
}
