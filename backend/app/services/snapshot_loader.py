import json
import math
from pathlib import Path

# In Docker, data is mounted at /app/data
# In local dev, it's at the project root
BASE_DIR = Path(__file__).resolve().parents[3]
if (BASE_DIR / "data" / "snapshots").exists():
    SNAPSHOT_ROOT = BASE_DIR / "data" / "snapshots"
elif Path("/app/data/snapshots").exists():
    SNAPSHOT_ROOT = Path("/app/data/snapshots")
else:
    SNAPSHOT_ROOT = Path("data/snapshots")



def _sanitize(obj):
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return obj
    if isinstance(obj, dict):
        return {k: _sanitize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_sanitize(v) for v in obj]
    return obj


def list_snapshot_dates():
    if not SNAPSHOT_ROOT.exists():
        return []

    return sorted([d.name for d in SNAPSHOT_ROOT.iterdir() if d.is_dir()])


def load_snapshot_by_date(date: str):
    path = SNAPSHOT_ROOT / date / "snapshot.json"
    if not path.exists():
        raise FileNotFoundError("Snapshot not found")
    with open(path, "r", encoding="utf-8") as f:
        return _sanitize(json.load(f))


def load_market_summary_by_date(date: str):
    path = SNAPSHOT_ROOT / date / "market_summary.json"
    if not path.exists():
        raise FileNotFoundError("Market summary not found")
    with open(path, "r", encoding="utf-8") as f:
        return _sanitize(json.load(f))


def load_latest_snapshot():
    dates = list_snapshot_dates()
    if not dates:
        raise FileNotFoundError("No snapshots found")
    snapshot = load_snapshot_by_date(dates[-1])
    print("FULL SNAPSHOT KEYS:", snapshot.keys())
    decisions = snapshot.get("decisions", [])
    itc_snapshot = None
    for d in decisions:
        if isinstance(d, dict) and d.get("stock") == "ITC":
            itc_snapshot = d
            break
    print("ITC SNAPSHOT:", itc_snapshot)
    return snapshot


def load_latest_market_summary():
    dates = list_snapshot_dates()
    if not dates:
        raise FileNotFoundError("No snapshots found")
    return load_market_summary_by_date(dates[-1])


def load_latest_reasoning_story(symbol: str):
    dates = list_snapshot_dates()
    if not dates:
        raise FileNotFoundError("No snapshots found")
    return load_reasoning_story_by_date(symbol, dates[-1])


def load_reasoning_story_by_date(symbol: str, date: str):
    snapshot = load_snapshot_by_date(date)
    decision = _find_decision(snapshot, symbol)
    if not decision:
        raise FileNotFoundError("Stock not found in snapshot")

    filename = _reasoning_filename(decision)
    path = SNAPSHOT_ROOT / date / "reasoning" / filename
    if not path.exists():
        raise FileNotFoundError("Reasoning story not found")

    with open(path, "r", encoding="utf-8") as f:
        return _sanitize(json.load(f))


def _find_decision(snapshot: dict, symbol: str):
    decisions = snapshot.get("decisions", [])
    target = symbol.strip().upper()

    for decision in decisions:
        stock = str(decision.get("stock") or "").upper()
        sym = str(decision.get("symbol") or "").upper()
        if stock == target or sym == target:
            return decision
    return None


def _reasoning_filename(decision: dict) -> str:
    symbol = decision.get("symbol")
    if symbol:
        base = str(symbol).replace(".", "_")
    else:
        base = str(decision.get("stock") or "UNKNOWN").replace(" ", "_")

    cleaned = "".join(ch for ch in base.upper() if ch.isalnum() or ch == "_")
    return f"{cleaned}.json"
