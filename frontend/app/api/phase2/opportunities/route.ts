import { NextResponse } from "next/server";
import { getOpportunitiesLocal } from "@/lib/local-data";

export async function GET() {
  return NextResponse.json(await getOpportunitiesLocal());
}
