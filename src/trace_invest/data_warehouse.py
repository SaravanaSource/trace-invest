from pathlib import Path
import json
from typing import Dict, Any

ROOT = Path("data/warehouse")
ROOT.mkdir(parents=True, exist_ok=True)


def write_financials(symbol: str, payload: Dict[str, Any]):
    p = ROOT / "financials"
    p.mkdir(parents=True, exist_ok=True)
    out = p / f"{symbol.replace('.', '_').upper()}.json"
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return out


def write_prices(symbol: str, payload: Any):
    p = ROOT / "prices"
    p.mkdir(parents=True, exist_ok=True)
    out = p / f"{symbol.replace('.', '_').upper()}.json"
    out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return out
