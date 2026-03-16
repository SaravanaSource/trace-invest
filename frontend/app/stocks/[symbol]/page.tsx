"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Card } from "@/components/ui/Card";
import { getLatestSnapshot } from "@/lib/api";

type StockData = any;

type NarrativeView = {
  summary: string;
  details: string[];
};

function buildSystemView(data: StockData) {
  const reasons: string[] = [];

  if (data.stability?.stability_band) {
    reasons.push(`Stability is ${data.stability.stability_band}`);
  }

  if (data.valuation?.valuation_sanity) {
    reasons.push(`Valuation is ${data.valuation.valuation_sanity}`);
  }

  if (data.overall_risk) {
    reasons.push(`Overall risk is ${data.overall_risk}`);
  }

  return {
    decision: data.decision_zone,
    masterBand: data.master?.master_band,
    masterScore: data.master?.master_score,
    confidence: data.quality?.confidence_band,
    reasons,
  };
}

function normalizeNarrative(narrative: any): NarrativeView {
  if (!narrative) {
    return { summary: "No narrative available", details: [] };
  }

  if (typeof narrative === "string") {
    return { summary: narrative, details: [] };
  }

  const summary = narrative.summary || "No narrative available";
  const details: string[] = Array.isArray(narrative.details)
    ? narrative.details
    : narrative.details
    ? [String(narrative.details)]
    : [];

  return { summary, details };
}

function formatBandChanges(bandChanges: Record<string, string> | undefined) {
  if (!bandChanges) {
    return [];
  }

  const labelMap: Record<string, string> = {
    valuation: "Valuation",
    stability: "Stability",
    governance: "Governance",
  };

  return Object.entries(labelMap)
    .filter(([key]) => bandChanges[key])
    .map(([key, label]) => `${label} ${bandChanges[key].toLowerCase()}`);
}

export default function StockDetailPage() {
  const params = useParams();
  const symbol = params.symbol as string;

  const [data, setData] = useState<StockData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getLatestSnapshot()
      .then((res) => {
        const decisions = Array.isArray(res?.decisions) ? res.decisions : [];
        const match = decisions.find((decision: any) => {
          const stock = String(decision?.stock || "").toUpperCase();
          const sym = String(decision?.symbol || "").toUpperCase();
          const requested = String(symbol || "").toUpperCase();
          return stock === requested || sym === requested;
        });

        setData(match || null);
      })
      .catch(() => setData(null))
      .finally(() => setLoading(false));
  }, [symbol]);

  if (loading) {
    return <div className="p-6 text-white/60">Loading...</div>;
  }

  if (!data) {
    return <div className="p-6 text-white/60">No data available</div>;
  }

  const systemView = buildSystemView(data);
  const narrative = normalizeNarrative(data.narrative);
  const delta = data.delta || {};
  const bandChanges = formatBandChanges(delta.band_changes);

  return (
    <div className="p-6 space-y-6 text-white">
      <div>
        <h1 className="text-2xl font-bold">{symbol}</h1>
        <div className="text-sm text-white/60">
          Snapshot at {data.timestamp}
        </div>
      </div>

      <Card>
        <h2 className="text-lg font-semibold mb-2">Narrative</h2>
        <p className="text-white/80">{narrative.summary}</p>
        {narrative.details.length > 0 && (
          <details className="mt-3 text-white/70">
            <summary className="cursor-pointer">Narrative details</summary>
            <ul className="list-disc pl-5 mt-2 space-y-1">
              {narrative.details.map((item, index) => (
                <li key={index}>{item}</li>
              ))}
            </ul>
          </details>
        )}
      </Card>

      <Card>
        <h2 className="text-lg font-semibold mb-2">
          What Changed Since Last Snapshot
        </h2>
        <p className="text-white/80">
          {delta.change_summary || "No change summary available"}
        </p>
        <div className="mt-3 space-y-1 text-white/70">
          {delta.decision_change && delta.decision_change !== "UNCHANGED" && (
            <div>Decision: {delta.decision_change}</div>
          )}
          {delta.risk_change && delta.risk_change !== "UNCHANGED" && (
            <div>Risk: {delta.risk_change}</div>
          )}
          {bandChanges.map((change, index) => (
            <div key={index}>{change}</div>
          ))}
        </div>
      </Card>

      <Card>
        <h2 className="text-lg font-semibold mb-3">System View</h2>
        <div className="mb-2">
          This stock is in{" "}
          <span className="font-semibold">{systemView.decision}</span> zone
          because:
        </div>

        <ul className="list-disc pl-5 text-white/70 space-y-1">
          {systemView.reasons.map((r, i) => (
            <li key={i}>{r}</li>
          ))}
        </ul>

        <div className="mt-4 text-white/70">
          Master Band:{" "}
          <span className="font-semibold">
            {systemView.masterBand} ({systemView.masterScore})
          </span>
        </div>

        <div className="text-white/70">
          Confidence Level:{" "}
          <span className="font-semibold">
            {systemView.confidence || "UNKNOWN"}
          </span>
        </div>
      </Card>
    </div>
  );
}
