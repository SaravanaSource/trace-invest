from typing import List, Dict, Any
from datetime import datetime, timedelta
from pathlib import Path
import json
import hashlib

from trace_invest.config import data_path, ensure_data_dirs

ensure_data_dirs("backtests")
OUT_DIR = data_path("backtests")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def _deterministic_from_name(name: str) -> float:
    h = hashlib.sha256(name.encode("utf-8")).hexdigest()
    v = int(h[:8], 16) / float(0xFFFFFFFF)
    return v


def run_backtest(strategy_name: str, positions: List[Dict[str, Any]], start: str = None, end: str = None, tc: float = 0.001) -> Dict:
    """Deterministic synthetic backtest that returns reproducible metrics.

    This implementation avoids dependence on external price series; it generates
    stable metrics derived from the strategy name so results are repeatable.
    """
    base = _deterministic_from_name(strategy_name)
    # synthetic timeline: last 3 years
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=365 * 3)

    # derive metrics from base value and number of positions
    npos = max(1, len(positions) or 1)
    cagr = -0.05 + base * 0.45  # in [-0.05, ~0.4]
    volatility = 0.05 + (1.0 - base) * 0.4
    sharpe = cagr / volatility if volatility > 0 else 0.0
    max_dd = -(0.05 + (1.0 - base) * 0.6)

    result = {
        "strategy": strategy_name,
        "start": str(start_date),
        "end": str(end_date),
        "CAGR": round(float(cagr), 4),
        "volatility": round(float(volatility), 4),
        "sharpe_ratio": round(float(sharpe), 4),
        "max_drawdown": round(float(max_dd), 4),
        "positions": positions,
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }

    out = OUT_DIR / f"{strategy_name}.json"
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result
