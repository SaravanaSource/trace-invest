from pathlib import Path
import json
from typing import List


def load_stock_history(symbol: str) -> List[dict]:
    symbol = symbol.upper()
    path = Path("data") / "history" / f"{symbol}.json"
    if not path.exists():
        return []

    try:
        return json.loads(path.read_text())
    except Exception:
        return []
