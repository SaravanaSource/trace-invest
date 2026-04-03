import { NextResponse } from "next/server";
import { getLatestSnapshotLocal } from "@/lib/local-data";

export async function GET() {
  const snapshot = await getLatestSnapshotLocal();
  return NextResponse.json(snapshot.decisions || []);
}
