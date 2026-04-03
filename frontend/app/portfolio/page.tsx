import { getPortfolio } from "@/lib/api";

export default async function PortfolioPage() {
  const portfolio = await getPortfolio();

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">Portfolio Builder</h1>
      <div className="mt-4">Cash: {portfolio.cash}</div>
      <ul className="mt-4 space-y-2">
        {(portfolio.positions || []).map((position: any) => (
          <li
            key={position.symbol}
            className="flex justify-between rounded bg-slate-800 p-2"
          >
            <div>{position.symbol}</div>
            <div className="font-semibold">{position.weight}</div>
          </li>
        ))}
      </ul>
    </div>
  );
}
