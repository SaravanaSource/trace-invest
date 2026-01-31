const API_BASE = "http://localhost:8000";


export async function getStocks() {
  const res = await fetch(`${API_BASE}/stocks`);
  if (!res.ok) throw new Error("Failed to fetch stocks");
  return res.json();
}
