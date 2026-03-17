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

export async function getOpportunities() {
  const res = await fetch(`${API_BASE}/phase2/opportunities`);
  if (!res.ok) throw new Error("Failed to fetch opportunities");
  return res.json();
}

export async function getPortfolio() {
  const res = await fetch(`${API_BASE}/portfolio`);
  if (!res.ok) throw new Error("Failed to fetch portfolio");
  return res.json();
}

export async function getWatchlists() {
  const res = await fetch(`${API_BASE}/watchlist/list`);
  if (!res.ok) throw new Error("Failed to fetch watchlists");
  return res.json();
}

export async function createWatchlist(payload: { name: string; symbols: string[] }) {
  const res = await fetch(`${API_BASE}/watchlist/create`, { method: "POST", body: JSON.stringify(payload), headers: { "Content-Type": "application/json" } });
  if (!res.ok) throw new Error("Failed to create watchlist");
  return res.json();
}

export async function getAdminMetrics() {
  const res = await fetch(`${API_BASE}/admin/metrics`);
  if (!res.ok) throw new Error("Failed to fetch admin metrics");
  return res.json();
}

export async function getAlphaResults() {
  const res = await fetch(`${API_BASE}/alpha/results`);
  if (!res.ok) throw new Error("Failed to fetch alpha results");
  return res.json();
}

export async function runAlphaNow(background = true) {
  const res = await fetch(`${API_BASE}/alpha/run`, { method: "POST", body: JSON.stringify({ background }), headers: { "Content-Type": "application/json" } });
  if (!res.ok) throw new Error("Failed to trigger alpha run");
  return res.json();
}

export async function getAlerts() {
  const res = await fetch(`${API_BASE}/phase2/alerts`);
  if (!res.ok) throw new Error("Failed to fetch alerts");
  return res.json();
}
