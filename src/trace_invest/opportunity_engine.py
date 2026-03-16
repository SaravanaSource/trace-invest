from pathlib import Path
import json
from typing import Dict, List

DATA_SIGNALS = Path("data/signals")
DATA_SIGNALS.mkdir(parents=True, exist_ok=True)


def build_opportunities(signals_map: Dict[str, List[Dict]], top_n: int = 50) -> List[Dict]:
    """Build and persist ranked opportunities from signals_map.

    Writes `data/signals/top_opportunities.json` and returns the list.
    """
    rows = []
    for sym, sigs in signals_map.items():
        score = 0.0
        for s in sigs:
            try:
                score += float(s.get("signal_strength") or 0)
            except Exception:
                continue
        rows.append({"symbol": sym, "score": round(score, 2), "signals": sigs})

    rows.sort(key=lambda r: r["score"], reverse=True)
    out = rows[:top_n]

    path = DATA_SIGNALS / "top_opportunities.json"
    path.write_text(json.dumps({"generated": True, "count": len(out), "rows": out}, indent=2), encoding="utf-8")
    return out
