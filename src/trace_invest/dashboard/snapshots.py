from pathlib import Path
import json
from typing import List, Dict

SNAPSHOT_DIR = Path("data/snapshots")


def list_snapshots() -> List[Path]:
    if not SNAPSHOT_DIR.exists():
        return []

    dated_dirs = [
        d for d in SNAPSHOT_DIR.iterdir()
        if d.is_dir()
    ]

    if not dated_dirs:
        return []

    latest_dir = sorted(dated_dirs, reverse=True)[0]
    snapshot_file = latest_dir / "snapshot.json"

    if snapshot_file.exists():
        return [snapshot_file]

    return []


def load_snapshot(path: Path) -> Dict:
    return json.loads(path.read_text())
