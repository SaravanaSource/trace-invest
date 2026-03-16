import { Card } from "@/components/ui/Card";
import { getStockReasoning } from "@/lib/api";

function renderFacts(title: string, facts: any[]) {
  if (!facts || facts.length === 0) {
    return <div className="text-white/60">No data</div>;
  }

  return (
    <div className="space-y-2">
      <div className="text-sm text-white/60">{title}</div>
      <ul className="space-y-2">
        {facts.map((fact, index) => (
          <li key={index} className="border border-white/10 rounded-lg p-3">
            <div className="font-semibold text-white">{fact.name}</div>
            <div className="text-sm text-white/70">
              Status: {fact.status || "UNKNOWN"} | Risk: {fact.risk || "UNKNOWN"}
            </div>
            {fact.explanation && (
              <div className="text-sm text-white/70 mt-1">
                {fact.explanation}
              </div>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default async function ReasoningStoryPage({
  params,
}: {
  params: { symbol: string };
}) {
  const story = await getStockReasoning(params.symbol);

  const metadata = story.metadata || {};
  const facts = story.observed_facts || {};
  const rules = story.interpretation_rules || [];
  const aggregation = story.aggregation_logic || {};
  const delta = story.delta_interpretation || {};
  const verdict = story.final_verdict || {};
  const guidance = story.verification_guidance || [];

  return (
    <div className="p-6 space-y-6 text-white">
      <div>
        <h1 className="text-2xl font-bold">Reasoning Story</h1>
        <div className="text-sm text-white/60">
          {metadata.stock} ({metadata.symbol}) — {metadata.run_date}
        </div>
      </div>

      <Card>
        <h2 className="text-lg font-semibold mb-2">1. What was evaluated</h2>
        <div className="text-white/70">
          {(story.evaluation_scope?.categories || []).join(", ") ||
            "No scope available"}
        </div>
      </Card>

      <Card>
        <h2 className="text-lg font-semibold mb-4">2. What was observed</h2>
        <div className="space-y-4">
          {renderFacts("Governance", facts.governance)}
          {renderFacts("Stability", facts.stability)}
          {renderFacts("Valuation", facts.valuation)}
          {renderFacts("Fraud", facts.fraud)}
          {renderFacts("Other", facts.other)}
        </div>
      </Card>

      <Card>
        <h2 className="text-lg font-semibold mb-4">3. How it was interpreted</h2>
        <ul className="space-y-3 text-white/80">
          {rules.map((rule: any, index: number) => (
            <li key={index} className="border border-white/10 rounded-lg p-3">
              <div className="font-semibold">{rule.statement}</div>
              <div className="text-sm text-white/70 mt-1">
                Inputs: {JSON.stringify(rule.inputs || {})}
              </div>
              <div className="text-sm text-white/70">
                Result: {JSON.stringify(rule.result || {})}
              </div>
            </li>
          ))}
        </ul>
      </Card>

      <Card>
        <h2 className="text-lg font-semibold mb-4">4. Aggregation logic</h2>
        <pre className="text-sm text-white/70 whitespace-pre-wrap">
          {JSON.stringify(aggregation, null, 2)}
        </pre>
      </Card>

      <Card>
        <h2 className="text-lg font-semibold mb-4">5. What changed</h2>
        <div className="text-white/80">
          {delta.change_summary || "No change summary available"}
        </div>
        {Array.isArray(delta.changes) && delta.changes.length > 0 && (
          <ul className="list-disc pl-5 mt-2 text-white/70 space-y-1">
            {delta.changes.map((change: string, index: number) => (
              <li key={index}>{change}</li>
            ))}
          </ul>
        )}
        {delta.verdict_impact && (
          <div className="text-white/70 mt-2">
            Verdict impact: {delta.verdict_impact}
          </div>
        )}
      </Card>

      <Card>
        <h2 className="text-lg font-semibold mb-4">6. Final verdict</h2>
        <div className="text-white/80">
          Decision zone: {verdict.decision_zone || "UNKNOWN"}
        </div>
        <div className="text-white/80">
          Overall risk: {verdict.overall_risk || "UNKNOWN"}
        </div>
        {Array.isArray(verdict.primary_reasons) && (
          <ul className="list-disc pl-5 mt-2 text-white/70 space-y-1">
            {verdict.primary_reasons.map((reason: string, index: number) => (
              <li key={index}>{reason}</li>
            ))}
          </ul>
        )}
        {Array.isArray(verdict.uncertainties) && verdict.uncertainties.length > 0 && (
          <div className="mt-3 text-white/70">
            Uncertainties: {verdict.uncertainties.join(", ")}
          </div>
        )}
      </Card>

      <Card>
        <h2 className="text-lg font-semibold mb-4">7. How to verify</h2>
        <ul className="list-disc pl-5 text-white/70 space-y-1">
          {guidance.map((item: string, index: number) => (
            <li key={index}>{item}</li>
          ))}
        </ul>
      </Card>
    </div>
  );
}
