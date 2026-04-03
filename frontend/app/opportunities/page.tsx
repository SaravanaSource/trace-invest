import { getOpportunities } from "@/lib/api";

export default async function OpportunitiesPage() {
  const data = await getOpportunities();

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">Opportunity Scanner</h1>
      <ul className="mt-4 space-y-3">
        {data.map((row: any, idx: number) => (
          <li key={`${row.symbol}-${idx}`} className="rounded bg-slate-800 p-3">
            <div className="flex justify-between">
              <div className="font-semibold">{row.symbol}</div>
              <div>{Number(row.score || 0).toFixed(1)}</div>
            </div>
            <div className="mt-2 text-sm text-slate-400">
              {(row.signals || []).map((signal: any) => (
                <div key={signal.signal_name}>
                  {signal.signal_name}: {Number(signal.signal_strength || 0).toFixed(2)}
                </div>
              ))}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
