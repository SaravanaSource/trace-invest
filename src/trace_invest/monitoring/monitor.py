from pathlib import Path
import json
from datetime import datetime

DATA_DIR = Path(__file__).resolve().parents[3] / "data"
MON = DATA_DIR / "monitoring"
MON.mkdir(parents=True, exist_ok=True)


def record_job(name: str, status: str, details: dict = None):
    p = MON / "jobs.json"
    data = {"jobs": []}
    if p.exists():
        try:
            data = json.loads(p.read_text())
        except Exception:
            data = {"jobs": []}
    entry = {"name": name, "status": status, "details": details or {}, "ts": datetime.utcnow().isoformat()+"Z"}
    data.setdefault("jobs", []).append(entry)
    p.write_text(json.dumps(data, indent=2))
    return entry
