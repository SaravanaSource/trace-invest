"use client";

import Link from "next/link";

export default function HeaderBar({
  title,
  generatedAt,
  nextUpdateText,
}: {
  title: string;
  generatedAt?: string | null;
  nextUpdateText?: string;
}) {
  const lastUpdatedText = generatedAt
    ? new Date(generatedAt).toLocaleString()
    : "N/A";

  return (
    <div className="mb-8 flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
      <div>
        <h1 className="text-3xl font-semibold text-white">{title}</h1>
        <div className="mt-2 text-sm text-textSecondary">
          Next update in {nextUpdateText || "Weekly"} | Last updated:{" "}
          {lastUpdatedText}
        </div>
      </div>
      <div className="flex flex-wrap items-center gap-3">
        <Link href="/alpha-lab/signals" className="secondary-cta">
          Signals
        </Link>
        <Link href="/alpha-lab/strategies" className="secondary-cta">
          Strategies
        </Link>
        <Link href="/alpha-lab/backtests" className="secondary-cta">
          Backtests
        </Link>
        <form method="post" action="/api/run-alpha">
          <button type="submit" className="primary-cta">
            Run Analysis
          </button>
        </form>
      </div>
    </div>
  );
}
