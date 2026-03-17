"use client";
import { useEffect, useState } from "react";
import { getAdminMetrics, getAlphaResults, runAlphaNow } from "@/lib/api";

export default function AdminPage() {
  const [metrics, setMetrics] = useState<any>(null);
  const [results, setResults] = useState<any[]>([]);

  useEffect(() => {
    fetchMetrics();
    fetchResults();
  }, []);

  async function fetchMetrics() {
    try {
      const m = await getAdminMetrics();
      setMetrics(m);
    } catch (e) {
      console.error(e);
    }
  }

  async function fetchResults() {
    try {
      const r = await getAlphaResults();
      setResults(r.results || []);
    } catch (e) {
      console.error(e);
    }
  }

  async function trigger() {
    try {
      await runAlphaNow(true);
      alert("Alpha pipeline scheduled");
    } catch (e) {
      console.error(e);
    }
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">Admin</h1>
      <div className="mt-4">
        <button onClick={trigger} className="px-3 py-2 bg-green-600 rounded">Run Alpha (background)</button>
      </div>

      <div className="mt-6">
        <h2 className="font-semibold">Metrics</h2>
        <pre className="mt-2 bg-slate-900 p-3 rounded">{JSON.stringify(metrics, null, 2)}</pre>
      </div>

      <div className="mt-6">
        <h2 className="font-semibold">Recent Alpha Results</h2>
        <ul className="mt-2 space-y-2">
          {results.map((r: any) => (
            <li key={r.id} className="p-2 bg-slate-800 rounded">
              <div className="font-semibold">{r.strategy}</div>
              <div className="text-sm">CAGR: {r.result?.CAGR} &nbsp; Sharpe: {r.result?.sharpe_ratio}</div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
