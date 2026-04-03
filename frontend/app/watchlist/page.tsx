"use client";

import { useEffect, useState } from "react";
import { createWatchlist, getWatchlists } from "@/lib/api";

type Watchlist = {
  id: number;
  name: string;
  symbols: string[];
};

export default function WatchlistPage() {
  const [lists, setLists] = useState<Watchlist[]>([]);
  const [name, setName] = useState("");
  const [symbols, setSymbols] = useState("");

  useEffect(() => {
    async function load() {
      try {
        const res = await getWatchlists();
        setLists(res.watchlists || []);
      } catch (error) {
        console.error(error);
      }
    }

    load();
  }, []);

  async function add() {
    try {
      await createWatchlist({
        name,
        symbols: symbols
          .split(",")
          .map((symbol) => symbol.trim())
          .filter(Boolean),
      });
      const res = await getWatchlists();
      setLists(res.watchlists || []);
      setName("");
      setSymbols("");
    } catch (error) {
      console.error(error);
    }
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">Watchlists</h1>

      <div className="mt-4 flex flex-wrap gap-2">
        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="List name"
          className="rounded border border-white/10 bg-slate-900 px-3 py-2"
        />
        <input
          value={symbols}
          onChange={(e) => setSymbols(e.target.value)}
          placeholder="comma separated symbols"
          className="rounded border border-white/10 bg-slate-900 px-3 py-2"
        />
        <button onClick={add} className="rounded bg-emerald-500 px-3 py-2 text-black">
          Create
        </button>
      </div>

      <ul className="mt-6 space-y-3">
        {lists.map((list) => (
          <li key={list.id} className="rounded bg-slate-800 p-3">
            <div className="font-semibold">{list.name}</div>
            <div className="text-sm text-muted">{(list.symbols || []).join(", ")}</div>
          </li>
        ))}
      </ul>
    </div>
  );
}
