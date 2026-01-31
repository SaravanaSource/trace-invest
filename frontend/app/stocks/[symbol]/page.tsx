"use client";

import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { Stat } from "@/components/ui/Stat";
import { Card } from "@/components/ui/Card";

export default function StockPage() {
  const { symbol } = useParams() as { symbol: string };
  const [stock, setStock] = useState<any>(null);

  useEffect(() => {
    fetch(`http://localhost:8000/stocks/${symbol}`)
      .then((r) => r.json())
      .then(setStock);
  }, [symbol]);

  if (!stock) return <p>Loading...</p>;

  return (
    <div className="space-y-8">
      <h1 className="text-4xl font-bold">{stock.stock}</h1>

      <div className="grid grid-cols-3 gap-6">
        <Stat
          label="Decision"
          value={stock.decision_zone}
          tone={stock.decision_zone === "EXIT" ? "bad" : "good"}
        />
        <Stat
          label="Risk"
          value={stock.overall_risk}
          tone={
            stock.overall_risk === "HIGH"
              ? "bad"
              : stock.overall_risk === "MEDIUM"
              ? "warn"
              : "good"
          }
        />
        <Stat
          label="Conviction"
          value={stock.conviction_score}
        />
      </div>

      <Card>
        <h3 className="font-semibold mb-2">Narrative</h3>
        {stock.narrative}
      </Card>

      <div className="grid grid-cols-3 gap-6">
        <Stat
          label="Master"
          value={`${stock.validation.master.master_score}`}
        />
        <Stat
          label="Governance"
          value={stock.validation.governance.governance_band}
        />
        <Stat
          label="Stability"
          value={stock.validation.stability.stability_band}
        />
      </div>
    </div>
  );
}
