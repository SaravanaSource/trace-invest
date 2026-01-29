import json
import math
from pathlib import Path

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
    return load_snapshot_by_date(dates[-1])


def load_latest_market_summary():
    dates = list_snapshot_dates()
    if not dates:
        raise FileNotFoundError("No snapshots found")
    return load_market_summary_by_date(dates[-1])
