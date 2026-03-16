"use client"
import React, { useEffect, useState } from "react";

export default function FactorExplorerPage() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/research/factors")
      .then((r) => r.json())
      .then((j) => setData(j))
      .catch(() => setData({ factors: [] }))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div style={{padding:20}}>Loading factors...</div>;

  return (
    <div style={{padding:20}}>
      <h1>Factor Explorer</h1>
      {data?.factors?.length ? (
        data.factors.map((f: any) => (
          <div key={f.symbol} style={{marginBottom:12,border:'1px solid #ddd',padding:8}}>
            <strong>{f.symbol}</strong>
            <pre style={{whiteSpace:'pre-wrap'}}>{JSON.stringify(f.factors || f, null, 2)}</pre>
          </div>
        ))
      ) : (
        <div>No factor files found</div>
      )}
    </div>
  );
}
