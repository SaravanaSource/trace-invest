"use client"
import React, { useEffect, useState } from "react";

export default function StrategyLabPage() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/research/strategies")
      .then((r) => r.json())
      .then((j) => setData(j))
      .catch(() => setData({ strategies: [] }))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div style={{padding:20}}>Loading strategies...</div>;

  return (
    <div style={{padding:20}}>
      <h1>Strategy Lab</h1>
      {data?.strategies?.length ? (
        data.strategies.map((s: any) => (
          <div key={s.name} style={{marginBottom:12,border:'1px solid #ddd',padding:8}}>
            <strong>{s.name}</strong>
            <pre style={{whiteSpace:'pre-wrap'}}>{JSON.stringify(s.results || s, null, 2)}</pre>
          </div>
        ))
      ) : (
        <div>No strategies found (run Phase-3 pipeline)</div>
      )}
    </div>
  );
}
