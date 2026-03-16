"use client"
import React, { useEffect, useState } from "react";

export default function PerformancePage() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/research/performance")
      .then((r) => r.json())
      .then((j) => setData(j))
      .catch(() => setData({ performance: [] }))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div style={{padding:20}}>Loading performance reports...</div>;

  return (
    <div style={{padding:20}}>
      <h1>Performance Reports</h1>
      {data?.performance?.length ? (
        data.performance.map((p: any, i: number) => (
          <div key={i} style={{marginBottom:12,border:'1px solid #ddd',padding:8}}>
            <pre style={{whiteSpace:'pre-wrap'}}>{JSON.stringify(p, null, 2)}</pre>
          </div>
        ))
      ) : (
        <div>No performance reports found</div>
      )}
    </div>
  );
}
