from pathlib import Path
import json
from typing import List, Dict

SNAPSHOT_DIR = Path("data/snapshots")


def list_snapshots() -> List[Path]:
    if not SNAPSHOT_DIR.exists():
        return []
    return sorted(SNAPSHOT_DIR.glob("weekly_*.json"), reverse=True)


def load_snapshot(path: Path) -> Dict:
    return json.loads(path.read_text())

