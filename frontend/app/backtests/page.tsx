"use client"
import React, { useEffect, useState } from "react";

export default function BacktestsPage() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/research/backtests")
      .then((r) => r.json())
      .then((j) => setData(j))
      .catch(() => setData({ backtests: [] }))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div style={{padding:20}}>Loading backtests...</div>;

  return (
    <div style={{padding:20}}>
      <h1>Backtests</h1>
      {data?.backtests?.length ? (
        data.backtests.map((b: any, i: number) => (
          <div key={i} style={{marginBottom:12,border:'1px solid #ddd',padding:8}}>
            <pre style={{whiteSpace:'pre-wrap'}}>{JSON.stringify(b, null, 2)}</pre>
          </div>
        ))
      ) : (
        <div>No backtests found</div>
      )}
    </div>
  );
}
