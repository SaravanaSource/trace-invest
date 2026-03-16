"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getLatestSnapshot } from "@/lib/api";

type Stock = {
  stock: string;
  decision_zone: string;
  conviction_score: number;
  overall_risk: string;
  delta?: {
    decision_change?: string;
  };
};

export default function StocksPage() {
  const [stocks, setStocks] = useState<Stock[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getLatestSnapshot()
      .then((res) => {
        if (Array.isArray(res?.decisions)) {
          setStocks(res.decisions);
        } else {
          console.error("Unexpected snapshot response:", res);
          setStocks([]);
        }
      })
      .catch((err) => {
        console.error(err);
        setError("Failed to load stocks");
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div className="p-6 text-white/60">Loading stocks…</div>;
  }

  if (error) {
    return <div className="p-6 text-red-400">{error}</div>;
  }

  return (
    <div className="p-6">
      <h1 className="text-xl font-semibold mb-4">Stocks</h1>

      <table className="w-full border-collapse">
        <thead>
          <tr className="text-left text-white/60 border-b border-white/10">
            <th className="py-2">Stock</th>
            <th className="py-2">Decision</th>
            <th className="py-2">Conviction</th>
            <th className="py-2">Risk</th>
          </tr>
        </thead>

        <tbody>
          {stocks.map((s) => (
            <Link
              key={s.stock || "unknown"}
              href={`/stocks/${encodeURIComponent(s.stock || "UNKNOWN")}`}
              className="contents"
            >
              <tr className="border-b border-white/5 hover:bg-white/5 cursor-pointer transition">
                <td className="py-2">{s.stock}</td>
                <td className="py-2">
                  <div className="flex items-center gap-2">
                    <span>{s.decision_zone}</span>
                    {s.delta?.decision_change === "UPGRADE" && (
                      <span className="text-xs uppercase border border-white/10 text-white/70 rounded px-2 py-0.5">
                        Upgraded
                      </span>
                    )}
                    {s.delta?.decision_change === "DOWNGRADE" && (
                      <span className="text-xs uppercase border border-white/10 text-white/70 rounded px-2 py-0.5">
                        Downgraded
                      </span>
                    )}
                  </div>
                </td>
                <td className="py-2">{s.conviction_score}</td>
                <td className="py-2">{s.overall_risk}</td>
              </tr>
            </Link>
          ))}
        </tbody>
      </table>
    </div>
  );
}
