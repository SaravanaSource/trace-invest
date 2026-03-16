import { getPortfolio } from "@/lib/api";

export default async function PortfolioPage() {
  let pf: any = { positions: [], cash: 0 };
  try {
    pf = await getPortfolio();
  } catch (e) {
    console.error(e);
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">Portfolio Builder</h1>
      <div className="mt-4">Cash: {pf.cash}</div>
      <ul className="mt-4 space-y-2">
        {pf.positions?.map((p: any) => (
          <li key={p.symbol} className="p-2 bg-slate-800 rounded flex justify-between">
            <div>{p.symbol}</div>
            <div className="font-semibold">{p.weight}</div>
          </li>
        ))}
      </ul>
    </div>
  );
}
