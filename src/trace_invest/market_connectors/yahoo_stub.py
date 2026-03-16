"""Lightweight market data updater stub that reads local history files.
This is deterministic and doesn't call external services.
"""
from pathlib import Path
import json
from datetime import datetime

DATA_DIR = Path(__file__).resolve().parents[3] / "data"
HISTORY = DATA_DIR / "history"


def daily_data_update():
    # read each history file and extract latest close -> write last_price.json
    out = {}
    for f in sorted(HISTORY.glob("*.json")):
        try:
            d = json.loads(f.read_text())
        except Exception:
            continue
        symbol = f.stem
        price = None
        if isinstance(d, dict):
            if "close" in d and isinstance(d["close"], list) and d["close"]:
                price = d["close"][-1]
            elif "prices" in d and isinstance(d["prices"], list) and d["prices"]:
                p = d["prices"][-1]
                if isinstance(p, dict) and "close" in p:
                    price = p["close"]
        elif isinstance(d, list) and d:
            price = d[-1]
        if price is not None:
            out[symbol] = {"last_price": price, "updated_at": datetime.utcnow().isoformat()+"Z"}

    (DATA_DIR / "market_prices.json").write_text(json.dumps(out, indent=2))
    return out
