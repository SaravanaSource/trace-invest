"use client";
import { useEffect, useState } from "react";
import { getWatchlists, createWatchlist } from "@/lib/api";

export default function WatchlistPage() {
  const [lists, setLists] = useState<any[]>([]);
  const [name, setName] = useState("");
  const [symbols, setSymbols] = useState("");

  useEffect(() => {
    fetchLists();
  }, []);

  async function fetchLists() {
    try {
      const res = await getWatchlists();
      setLists(res.watchlists || []);
    } catch (e) {
      console.error(e);
    }
  }

  async function add() {
    try {
      await createWatchlist({ name, symbols: symbols.split(",").map((s) => s.trim()).filter(Boolean) });
      setName("");
      setSymbols("");
      fetchLists();
    } catch (e) {
      console.error(e);
    }
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">Watchlists</h1>

      <div className="mt-4">
        <input value={name} onChange={(e) => setName(e.target.value)} placeholder="List name" className="p-2 mr-2" />
        <input value={symbols} onChange={(e) => setSymbols(e.target.value)} placeholder="comma separated symbols" className="p-2 mr-2" />
        <button onClick={add} className="px-3 py-2 bg-indigo-600 rounded">Create</button>
      </div>

      <ul className="mt-6 space-y-3">
        {lists.map((l: any) => (
          <li key={l.id} className="p-3 bg-slate-800 rounded">
            <div className="font-semibold">{l.name}</div>
            <div className="text-sm text-muted">{(l.symbols || []).join(", ")}</div>
          </li>
        ))}
      </ul>
    </div>
  );
}
