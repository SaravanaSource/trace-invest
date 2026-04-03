"use client";

import Link from "next/link";
import { useState } from "react";

export default function Card({
  card,
  index,
}: {
  card: any;
  index: number;
}) {
  const [hover, setHover] = useState(false);
  const [open, setOpen] = useState(false);
  const numericScore = Number(card.score ?? card.result?.score ?? 0);
  const showNumericScore = numericScore > 0;
  const confidence = (card.confidence || "Medium") as string;
  const risk = card.riskLevel || "Moderate";
  const isTop = index === 0;

  const scoreColor =
    numericScore >= 8
      ? "bg-positive text-black"
      : numericScore >= 6
        ? "bg-warning text-black"
        : "bg-negative text-white";

  const rawSummary =
    card.what ||
    card.summary ||
    (card.reasons && card.reasons.length
      ? card.reasons[0]
      : "Model-driven idea.");

  const mapSignalName = (value: string) => {
    if (!value) {
      return value;
    }

    const normalized = value.toLowerCase();
    if (normalized.includes("volatility_drop")) {
      return "Stabilizing price movement";
    }
    if (normalized.includes("momentum_breakout")) {
      return "Strong upward momentum";
    }
    return value.replace(/_/g, " ").replace(/\b\w/g, (char) => char.toUpperCase());
  };

  const summary = mapSignalName(rawSummary);
  const reliabilityLabel =
    card.unreliable || card.reliability === "low"
      ? "Under Evaluation"
      : "Emerging Signal";

  const renderConfidence = (value: string) => {
    const normalized = (value || "Medium").toLowerCase();
    if (normalized.includes("high")) {
      return (
        <div className="text-sm font-semibold text-white">
          <span className="text-amber-400">***</span>
          <span className="ml-2 muted">High</span>
        </div>
      );
    }
    if (normalized.includes("low")) {
      return (
        <div className="text-sm font-semibold text-white">
          <span className="text-amber-400">*..</span>
          <span className="ml-2 muted">Low</span>
        </div>
      );
    }
    return (
      <div className="text-sm font-semibold text-white">
        <span className="text-amber-400">**.</span>
        <span className="ml-2 muted">Medium</span>
      </div>
    );
  };

  return (
    <article
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      onClick={() => setOpen(!open)}
      role="button"
      className={`card-bg rounded-xl border border-borderSoft p-6 transition-transform duration-200 ${
        hover ? "translate-y-[-6px] shadow-xl" : ""
      } ${isTop ? "scale-105 ring-4 ring-yellow-400/20" : ""}`}
    >
      <div className="flex items-start justify-between gap-6">
        <div className="max-w-[65%]">
          <div className="text-xs muted">#{index + 1}</div>
          <div className="flex flex-wrap items-baseline gap-3">
            <div className="text-xl font-semibold md:text-2xl">{card.symbol}</div>
            <div className="text-sm muted">{card.name || ""}</div>
            {isTop ? (
              <div className="ml-1 inline-flex items-center gap-2 rounded-full bg-yellow-500/10 px-2 py-1 text-sm font-semibold">
                Top Pick Today
              </div>
            ) : null}
          </div>
          <div className="mt-3 text-lg font-bold leading-snug md:text-xl">
            {summary}
          </div>
          <div className="mt-2 text-sm text-white/70">{card.note || ""}</div>
        </div>

        <div className="text-right">
          {showNumericScore ? (
            <div
              className={`inline-flex items-center justify-center rounded-full px-3 py-1 text-lg font-bold ${scoreColor}`}
            >
              {numericScore.toFixed(1)}
            </div>
          ) : (
            <div className="inline-flex items-center justify-center rounded-full bg-surface px-3 py-1 text-sm font-semibold text-white">
              {reliabilityLabel}
            </div>
          )}

          <div className="mt-2 text-xs muted">
            {renderConfidence(confidence)}
            <div className="mt-1 muted">| {risk}</div>
          </div>
        </div>
      </div>

      <div className="mt-5">
        <div className="text-sm font-medium">Why it matters</div>
        <div className="mt-2 text-sm text-textSecondary">
          This stock is showing early signs of potential movement and is worth
          monitoring.
        </div>
        <ul className="mt-2 ml-5 list-disc space-y-1 text-sm">
          {(card.reasons || []).slice(0, 3).map((reason: any, reasonIndex: number) => (
            <li key={reasonIndex}>{reason}</li>
          ))}
        </ul>
      </div>

      <div className="mt-4 rounded-md bg-white/2 p-4">
        <div className="text-sm font-semibold">What to do</div>
        <div className="mt-1 text-sm text-textSecondary">
          Watch closely | potential opportunity forming.
        </div>
        <div className="mt-3 flex flex-wrap gap-3">
          <Link
            href={`/stocks/${encodeURIComponent(card.symbol)}`}
            onClick={(event) => event.stopPropagation()}
            className="secondary-cta"
          >
            See Full Analysis
          </Link>
          <Link
            href="/watchlist"
            onClick={(event) => event.stopPropagation()}
            className="primary-cta"
          >
            Add to Watchlist
          </Link>
        </div>
      </div>

      <div className="mt-3 text-xs muted">
        Horizon: 2-8 weeks | Confidence: {confidence} | Risk: {risk}
      </div>

      {open ? (
        <div className="mt-3 text-sm text-textSecondary">
          Expanded details: more context, links to backtests, and references to
          source data will appear here as the pipeline artifacts mature.
        </div>
      ) : null}
    </article>
  );
}
