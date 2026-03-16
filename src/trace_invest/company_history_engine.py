from pathlib import Path
import json
from typing import Dict, List, Optional

SNAPSHOT_ROOT = Path("data/snapshots")
HISTORY_ROOT = Path("data/history")
HISTORY_ROOT.mkdir(parents=True, exist_ok=True)


def build_company_history(symbol: str) -> Optional[Dict]:
    """Scan snapshots and build a deterministic history object for `symbol`.

    Output is written to `data/history/{SYMBOL}.json` and returned.
    """
    dates = sorted([d.name for d in SNAPSHOT_ROOT.iterdir() if d.is_dir()])
    if not dates:
        return None

    rows: List[Dict] = []
    for d in dates:
        path = SNAPSHOT_ROOT / d / "snapshot.json"
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue

        decisions = payload.get("decisions", [])
        for dec in decisions:
            sym = (dec.get("symbol") or dec.get("stock") or "").upper()
            if sym == symbol.upper():
                rows.append({
                    "date": d,
                    "conviction_score": dec.get("conviction_score"),
                    "decision_zone": dec.get("decision_zone"),
                    "overall_risk": dec.get("overall_risk"),
                })

    rows.sort(key=lambda r: r.get("date") or "")

    history = {"symbol": symbol.upper(), "rows": rows}

    out = HISTORY_ROOT / f"{symbol.replace('.','_').upper()}.json"
    out.write_text(json.dumps(history, indent=2, sort_keys=True), encoding="utf-8")
    return history
