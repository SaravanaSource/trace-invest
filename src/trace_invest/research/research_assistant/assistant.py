from typing import Dict, Any, List
from pathlib import Path
import json

DATA_HISTORY = Path("data/history")


def top_conviction_growth(n_years: int = 2, top_n: int = 10) -> List[Dict[str, Any]]:
    """Return symbols with largest conviction growth over past n_years using history rows."""
    rows = []
    for p in DATA_HISTORY.glob("*.json"):
        try:
            h = json.loads(p.read_text(encoding="utf-8"))
            sym = h.get("symbol")
            hist = h.get("rows", [])
            if len(hist) >= 2:
                last = float(hist[-1].get("conviction_score") or 0)
                prev = float(hist[0].get("conviction_score") or 0)
                growth = last - prev
                rows.append({"symbol": sym, "growth": growth, "last": last, "prev": prev})
        except Exception:
            continue
    rows.sort(key=lambda r: r["growth"], reverse=True)
    return rows[:top_n]


def summarize_company_trend(symbol: str) -> Dict[str, Any]:
    p = DATA_HISTORY / f"{symbol.replace('.','_').upper()}.json"
    if not p.exists():
        return {"symbol": symbol, "error": "no history"}
    h = json.loads(p.read_text(encoding="utf-8"))
    rows = h.get("rows", [])
    return {"symbol": symbol, "rows_count": len(rows), "latest": rows[-1] if rows else None}
from typing import Dict, Any, List
from pathlib import Path
import json

HISTORY = Path("data/history")


def highest_conviction_growth(top_n: int = 10) -> List[Dict[str, Any]]:
    rows = []
    for p in HISTORY.iterdir():
        if not p.is_file():
            continue
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            sym = data.get("symbol")
            r = data.get("rows", [])
            if len(r) >= 2:
                last = float(r[-1].get("conviction_score") or 0)
                prev = float(r[-2].get("conviction_score") or 0)
                rows.append({"symbol": sym, "delta": last - prev})
        except Exception:
            continue

    rows.sort(key=lambda x: x["delta"], reverse=True)
    return rows[:top_n]


def answer_query(q: str) -> Dict[str, Any]:
    q = q.lower()
    if "conviction growth" in q or "highest conviction" in q:
        top = highest_conviction_growth(10)
        return {"query": q, "answer": top}
    return {"query": q, "answer": "unsupported query"}
