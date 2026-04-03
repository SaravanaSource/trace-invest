import { NextResponse } from "next/server";
import { getAlertsLocal } from "@/lib/local-data";

export async function GET() {
  return NextResponse.json(await getAlertsLocal());
}
