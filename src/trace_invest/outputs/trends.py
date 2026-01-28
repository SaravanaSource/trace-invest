from pathlib import Path
import json
from typing import Dict, List

HISTORY_DIR = Path("data/history")


def compute_trend(symbol: str) -> Dict:
    path = HISTORY_DIR / f"{symbol}.json"

    if not path.exists():
        return {
            "trend": "NO_DATA",
            "delta": None,
        }

    try:
        data = json.loads(path.read_text())
    except Exception:
        return {
            "trend": "NO_DATA",
            "delta": None,
        }

    if len(data) < 2:
        return {
            "trend": "NO_DATA",
            "delta": None,
        }

    window = data[-4:]  # last 4 entries

    first = window[0].get("master_score")
    last = window[-1].get("master_score")

    if first is None or last is None:
        return {
            "trend": "NO_DATA",
            "delta": None,
        }

    delta = round(last - first, 1)

    if delta >= 5:
        label = "IMPROVING"
    elif delta <= -5:
        label = "DETERIORATING"
    else:
        label = "STABLE"

    return {
        "trend": label,
        "delta": delta,
    }

