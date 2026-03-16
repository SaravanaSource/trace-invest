const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000";

export async function getStocks() {
  const res = await fetch(`${API_BASE}/stocks`);

  if (!res.ok) {
    const text = await res.text();
    console.error("API /stocks failed:", res.status, text);
    throw new Error("Failed to fetch stocks");
  }

  return res.json();
}

export async function getMarketSummary() {
  const res = await fetch(`${API_BASE}/market/summary`);

  if (!res.ok) {
    const text = await res.text();
    console.error("API /market/summary failed:", res.status, text);
    throw new Error("Failed to fetch market summary");
  }

  return res.json();
}

export async function getLatestSnapshot() {
  const res = await fetch(`${API_BASE}/snapshots/snapshots`);

  if (!res.ok) {
    const text = await res.text();
    console.error("API /snapshots/snapshots failed:", res.status, text);
    throw new Error("Failed to fetch latest snapshot");
  }

  return res.json();
}

export async function getStockReasoning(symbol: string) {
  const res = await fetch(`${API_BASE}/stocks/${symbol}/reasoning`);

  if (!res.ok) {
    const text = await res.text();
    console.error("API /stocks/{symbol}/reasoning failed:", res.status, text);
    throw new Error("Failed to fetch reasoning story");
  }

  return res.json();
}
