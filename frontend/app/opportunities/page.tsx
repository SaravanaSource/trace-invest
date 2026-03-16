import { getOpportunities } from "@/lib/api";

export default async function OpportunitiesPage() {
  let data = [];
  try {
    data = await getOpportunities();
  } catch (e) {
    console.error(e);
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">Opportunity Scanner</h1>
      <ul className="mt-4 space-y-3">
        {data.map((r: any) => (
          <li key={r.symbol} className="p-3 bg-slate-800 rounded">
            <div className="flex justify-between">
              <div className="font-semibold">{r.symbol}</div>
              <div>{r.score}</div>
            </div>
            <div className="text-sm text-slate-400 mt-2">
              {r.signals?.map((s: any) => (<div key={s.signal_name}>{s.signal_name}: {s.signal_strength}</div>))}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
