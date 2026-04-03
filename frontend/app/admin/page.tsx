"use client";

import { useEffect, useState } from "react";
import { getAdminMetrics, getAlphaResults, runAlphaNow } from "@/lib/api";

type Metrics = {
  strategy_results?: number;
  queue_length?: number;
  snapshot_count?: number;
  latest_snapshot?: string | null;
  source?: string;
};

type AlphaResult = {
  id: number;
  strategy: string;
  result?: {
    CAGR?: number;
    sharpe_ratio?: number;
  };
};

export default function AdminPage() {
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [results, setResults] = useState<AlphaResult[]>([]);

  useEffect(() => {
    async function load() {
      try {
        const [metricsResponse, resultsResponse] = await Promise.all([
          getAdminMetrics(),
          getAlphaResults(),
        ]);
        setMetrics(metricsResponse);
        setResults(resultsResponse.results || []);
      } catch (error) {
        console.error(error);
      }
    }

    load();
  }, []);

  async function trigger() {
    try {
      const response = await runAlphaNow(true);
      alert(response.message || "Research mode refreshed");
    } catch (error) {
      console.error(error);
    }
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">Admin</h1>
      <div className="mt-4">
        <button onClick={trigger} className="rounded bg-green-600 px-3 py-2">
          Run Alpha
        </button>
      </div>

      <div className="mt-6">
        <h2 className="font-semibold">Metrics</h2>
        <pre className="mt-2 rounded bg-slate-900 p-3">
          {JSON.stringify(metrics, null, 2)}
        </pre>
      </div>

      <div className="mt-6">
        <h2 className="font-semibold">Recent Alpha Results</h2>
        <ul className="mt-2 space-y-2">
          {results.map((result) => (
            <li key={result.id} className="rounded bg-slate-800 p-2">
              <div className="font-semibold">{result.strategy}</div>
              <div className="text-sm">
                CAGR: {result.result?.CAGR ?? "N/A"} | Sharpe:{" "}
                {result.result?.sharpe_ratio ?? "N/A"}
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
