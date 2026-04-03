import { NextResponse } from "next/server";

export async function POST(request: Request) {
  const url = new URL(request.url);
  const background = url.searchParams.get("background") ?? "true";

  return NextResponse.json({
    status: "ready",
    background,
    message:
      "Local product mode is active. The existing alpha artifacts are available in the UI; full pipeline execution still requires the Python backend worker stack.",
  });
}
