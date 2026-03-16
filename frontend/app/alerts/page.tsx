import { getAlerts } from "@/lib/api";

export default async function AlertsPage() {
  let alerts = [];
  try {
    alerts = await getAlerts();
  } catch (e) {
    console.error(e);
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">Alert Center</h1>
      <ul className="mt-4 space-y-3">
        {alerts.map((a: any, idx: number) => (
          <li key={idx} className="p-3 bg-slate-800 rounded">
            <div className="flex justify-between">
              <div className="font-semibold">{a.symbol} — {a.alert_type}</div>
              <div className="text-sm text-slate-400">{a.severity}</div>
            </div>
            <div className="text-sm text-slate-300 mt-2">{a.reason}</div>
          </li>
        ))}
      </ul>
    </div>
  );
}
