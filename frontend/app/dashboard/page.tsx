import { Card } from "@/components/ui/Card";

export default function Dashboard() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Dashboard</h1>

      <div className="grid grid-cols-3 gap-6">
        <Card>Total Stocks</Card>
        <Card>Decision Zones</Card>
        <Card>Risk Bands</Card>
      </div>
    </div>
  );
}
