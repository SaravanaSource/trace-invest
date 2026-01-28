from pathlib import Path
import json
from typing import Dict


HISTORY_DIR = Path("data/history")
HISTORY_DIR.mkdir(parents=True, exist_ok=True)


def update_stock_history(decision: Dict, run_date: str):

    symbol = decision.get("stock")
    v = decision.get("validation", {})

    master = v.get("master", {})
    governance = v.get("governance", {})
    stability = v.get("stability", {})

    row = {
        "date": run_date,
        "decision_zone": decision.get("decision_zone"),
        "master_score": master.get("master_score"),
        "master_band": master.get("master_band"),
        "governance_band": governance.get("governance_band"),
        "stability_band": stability.get("stability_band"),
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

