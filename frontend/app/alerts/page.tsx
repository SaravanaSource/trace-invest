import { getAlerts } from "@/lib/api";

export default async function AlertsPage() {
  const alerts = await getAlerts();

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">Alert Center</h1>
      <ul className="mt-4 space-y-3">
        {alerts.map((alert: any, idx: number) => (
          <li key={idx} className="rounded bg-slate-800 p-3">
            <div className="flex justify-between">
              <div className="font-semibold">
                {alert.symbol} - {alert.alert_type}
              </div>
              <div className="text-sm text-slate-400">{alert.severity}</div>
            </div>
            <div className="mt-2 text-sm text-slate-300">
              {alert.reason || alert.message}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
