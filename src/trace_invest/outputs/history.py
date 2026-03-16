from pathlib import Path
import json
from typing import Dict


HISTORY_DIR = Path("data/history")
HISTORY_DIR.mkdir(parents=True, exist_ok=True)


def update_stock_history(decision: Dict, run_date: str):

    symbol = decision.get("stock")
    v = decision.get("validation", {})

    master = decision.get("master") or v.get("master", {})
    governance = decision.get("governance") or v.get("governance", {})
    stability = decision.get("stability") or v.get("stability", {})
    valuation = decision.get("valuation") or {}
    trend = decision.get("trend") or {}
    details = v.get("details", {})
    val_sanity = valuation.get("valuation_sanity")
    if val_sanity is None:
        val_detail = details.get("valuation_sanity") if isinstance(details, dict) else None
        if isinstance(val_detail, dict):
            val_sanity = val_detail.get("status")
        else:
            val_sanity = val_detail

    row = {
        "date": run_date,
        "decision_zone": decision.get("decision_zone"),
        "master_score": master.get("master_score"),
        "master_band": master.get("master_band"),
        "governance_band": governance.get("governance_band"),
        "stability_band": stability.get("stability_band"),
        "valuation_sanity": val_sanity,
        "overall_risk": decision.get("overall_risk"),
        "trend": trend.get("trend"),
    }

    path = HISTORY_DIR / f"{symbol}.json"

    if path.exists():
        try:
            data = json.loads(path.read_text())
        except Exception:
            data = []
    else:
        data = []

    data.append(row)
    path.write_text(json.dumps(data, indent=2))

