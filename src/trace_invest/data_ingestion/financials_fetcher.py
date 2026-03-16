from pathlib import Path
import json
from typing import Optional, Dict

RAW_DIR = Path("data/raw/fundamentals")


def fetch_financials_from_local(symbol: str) -> Optional[Dict]:
    """Deterministic: loads normalized financials from `data/raw/fundamentals`.

    Returns None if file not present or invalid JSON.
    """
    filename = f"{symbol.replace('.', '_').upper()}.json"
    path = RAW_DIR / filename
    if not path.exists():
        return None

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None

    # Minimal normalization hook: ensure expected top-level keys exist.
    normalized = {
        "symbol": data.get("symbol") or symbol,
        "financials": data.get("financials") or {},
        "metadata": data.get("metadata") or {},
    }
    return normalized
