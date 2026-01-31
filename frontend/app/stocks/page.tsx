"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

export default function StocksPage() {
  const [stocks, setStocks] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/stocks")
      .then((r) => r.json())
      .then((d) => {
        setStocks(d);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading stocks...</p>;

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Stocks</h1>

      <div className="bg-panel border border-border rounded-xl overflow-hidden">
        <table className="w-full">
          <thead className="bg-black/40 text-muted">
            <tr>
              <th className="p-3 text-left">Stock</th>
              <th className="p-3 text-left">Decision</th>
              <th className="p-3 text-left">Risk</th>
              <th className="p-3 text-left">Conviction</th>
            </tr>
          </thead>

          <tbody>
            {stocks.map((s) => (
              <tr
                key={s.stock}
                className="border-t border-border hover:bg-white/5"
              >
                <td className="p-3">
                  <Link
                    href={`/stocks/${s.stock}`}
                    className="text-good hover:underline"
                  >
                    {s.stock}
                  </Link>
                </td>
                <td className="p-3">{s.decision_zone}</td>
                <td className="p-3">{s.overall_risk}</td>
                <td className="p-3">{s.conviction_score}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
