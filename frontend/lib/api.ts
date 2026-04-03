const EXTERNAL_API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL ||
  process.env.NEXT_PUBLIC_API_URL ||
  "http://127.0.0.1:8000";

async function browserJson(path: string, init?: RequestInit) {
  const res = await fetch(path, {
    cache: "no-store",
    ...init,
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`${path} failed: ${res.status} ${text}`);
  }

  return res.json();
}

async function tryExternalJson(path: string) {
  const res = await fetch(`${EXTERNAL_API_BASE}${path}`, {
    cache: "no-store",
  });
  if (!res.ok) {
    throw new Error(`External API failed for ${path}`);
  }
  return res.json();
}

export async function getStocks() {
  if (typeof window !== "undefined") {
    return browserJson("/api/stocks");
  }

  const local = await import("./local-data");
  const snapshot = await local.getLatestSnapshotLocal();
  return snapshot.decisions || [];
}

export async function getMarketSummary() {
  if (typeof window !== "undefined") {
    return browserJson("/api/market/summary");
  }

  try {
    return await tryExternalJson("/market/summary");
  } catch {
    const local = await import("./local-data");
    return local.getMarketSummaryLocal();
  }
}

export async function getLatestSnapshot() {
  if (typeof window !== "undefined") {
    return browserJson("/api/snapshots/latest");
  }

  try {
    return await tryExternalJson("/snapshots/snapshots");
  } catch {
    const local = await import("./local-data");
    return local.getLatestSnapshotLocal();
  }
}

export async function getStockReasoning(symbol: string) {
  if (typeof window !== "undefined") {
    return browserJson(`/api/stocks/${encodeURIComponent(symbol)}/reasoning`);
  }

  try {
    return await tryExternalJson(`/stocks/${encodeURIComponent(symbol)}/reasoning`);
  } catch {
    const local = await import("./local-data");
    return local.getStockReasoningLocal(symbol);
  }
}

export async function getOpportunities() {
  if (typeof window !== "undefined") {
    return browserJson("/api/phase2/opportunities");
  }

  try {
    return await tryExternalJson("/phase2/opportunities");
  } catch {
    const local = await import("./local-data");
    return local.getOpportunitiesLocal();
  }
}

export async function getPortfolio() {
  if (typeof window !== "undefined") {
    return browserJson("/api/portfolio");
  }

  try {
    return await tryExternalJson("/portfolio");
  } catch {
    const local = await import("./local-data");
    return local.getPortfolioLocal();
  }
}

export async function getWatchlists() {
  if (typeof window !== "undefined") {
    return browserJson("/api/watchlist/list");
  }

  const local = await import("./local-data");
  return local.getWatchlistsLocal();
}

export async function createWatchlist(payload: {
  name: string;
  symbols: string[];
}) {
  if (typeof window !== "undefined") {
    return browserJson("/api/watchlist/create", {
      method: "POST",
      body: JSON.stringify(payload),
      headers: { "Content-Type": "application/json" },
    });
  }

  const local = await import("./local-data");
  return local.createWatchlistLocal(payload);
}

export async function getAdminMetrics() {
  if (typeof window !== "undefined") {
    return browserJson("/api/admin/metrics");
  }

  try {
    return await tryExternalJson("/admin/metrics");
  } catch {
    const local = await import("./local-data");
    return local.getAdminMetricsLocal();
  }
}

export async function getAlphaResults() {
  if (typeof window !== "undefined") {
    return browserJson("/api/alpha/results");
  }

  try {
    return await tryExternalJson("/alpha/results");
  } catch {
    const local = await import("./local-data");
    return local.getAlphaResultsLocal();
  }
}

export async function runAlphaNow(background = true) {
  if (typeof window !== "undefined") {
    return browserJson(`/api/run-alpha?background=${background ? "true" : "false"}`, {
      method: "POST",
    });
  }

  try {
    const res = await fetch(
      `${EXTERNAL_API_BASE}/alpha/run?background=${background ? "true" : "false"}`,
      { method: "POST", cache: "no-store" }
    );
    return res.json();
  } catch {
    return {
      status: "ready",
      mode: "local_artifacts",
      message:
        "Alpha pipeline execution requires the Python backend. Existing artifacts remain available in the UI.",
    };
  }
}

export async function getAlerts() {
  if (typeof window !== "undefined") {
    return browserJson("/api/phase2/alerts");
  }

  try {
    return await tryExternalJson("/phase2/alerts");
  } catch {
    const local = await import("./local-data");
    return local.getAlertsLocal();
  }
}
