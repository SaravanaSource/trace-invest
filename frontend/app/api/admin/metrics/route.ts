import { NextResponse } from "next/server";
import { getAdminMetricsLocal } from "@/lib/local-data";

export async function GET() {
  return NextResponse.json(await getAdminMetricsLocal());
}
