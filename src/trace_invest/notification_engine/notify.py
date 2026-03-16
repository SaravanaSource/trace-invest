from pathlib import Path
import json
from datetime import datetime
DATA_DIR = Path(__file__).resolve().parents[3] / "data"
ALERTS = DATA_DIR / "alerts"
ALERTS.mkdir(parents=True, exist_ok=True)


def notify_user(username: str, title: str, body: str):
    target = ALERTS / f"{username}.json"
    entry = {"title": title, "body": body, "ts": datetime.utcnow().isoformat()+"Z"}
    data = {"alerts": []}
    if target.exists():
        try:
            data = json.loads(target.read_text())
        except Exception:
            data = {"alerts": []}
    data.setdefault("alerts", []).append(entry)
    target.write_text(json.dumps(data, indent=2))
    # console fallback
    print(f"Notify {username}: {title} - {body}")
    return entry
