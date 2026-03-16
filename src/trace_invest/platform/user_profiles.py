from pathlib import Path
import json

DATA_DIR = Path(__file__).resolve().parents[3] / "data"
USERS_DIR = DATA_DIR / "users"
USERS_DIR.mkdir(parents=True, exist_ok=True)


def get_profile(username: str):
    p = USERS_DIR / f"{username}.profile.json"
    if not p.exists():
        return {"username": username, "preferences": {}}
    try:
        return json.loads(p.read_text())
    except Exception:
        return {"username": username, "preferences": {}}


def save_profile(username: str, profile: dict):
    p = USERS_DIR / f"{username}.profile.json"
    p.write_text(json.dumps(profile, indent=2))
    return profile
