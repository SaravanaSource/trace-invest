import json
from pathlib import Path
from math import sqrt
from datetime import datetime

DATA_DIR = Path(__file__).resolve().parents[3] / "data"
BACKTEST_DIR = DATA_DIR / "backtests"
RANK_DIR = DATA_DIR / "strategy_rankings"
RANK_DIR.mkdir(parents=True, exist_ok=True)


def _metrics_from_returns(returns):
    # returns: list of period returns (e.g., monthly)
    if not returns:
        return {"cagr": 0.0, "sharpe": 0.0, "max_dd": 0.0, "consistency": 0.0}
    n = len(returns)
    avg = sum(returns) / n
    # approximate CAGR from average periodic return assuming monthly
    cagr = (1 + avg) ** 12 - 1
    # sharpe: mean / std * sqrt(12)
    mean = avg
    var = sum((r - mean) ** 2 for r in returns) / n
    std = sqrt(var) if var > 0 else 0.0
    sharpe = (mean / std * sqrt(12)) if std > 0 else 0.0

    # max drawdown from cumulative
    cum = 1.0
    peak = 1.0
    max_dd = 0.0
    for r in returns:
        cum *= (1 + r)
        if cum > peak:
            peak = cum
        dd = (cum - peak) / peak
        if dd < max_dd:
            max_dd = dd

    # consistency: percent of positive months
    pos = len([r for r in returns if r > 0])
    consistency = pos / n
    return {"cagr": cagr, "sharpe": sharpe, "max_dd": max_dd, "consistency": consistency}


def rank_strategies(save_path: Path = None):
    rankings = []
    for f in sorted(BACKTEST_DIR.glob("*.json")):
        data = json.loads(f.read_text())
        name = data.get("strategy_name") or f.stem
        returns = data.get("monthly_returns") or data.get("returns") or []
        m = _metrics_from_returns(returns)
        # simple alpha score composition
        alpha = 100 * (0.4 * (m.get("sharpe", 0)) + 0.3 * m.get("cagr", 0) + 0.2 * m.get("consistency", 0) + 0.1 * max(0, -m.get("max_dd", 0)))
        rankings.append({
            "strategy": name,
            "alpha_score": round(alpha, 2),
            "CAGR": round(m["cagr"], 4),
            "sharpe": round(m["sharpe"], 4),
            "max_drawdown": round(m["max_dd"], 4),
            "consistency": round(m["consistency"], 4),
        })

    # deterministic sort: by alpha_score desc then name
    rankings = sorted(rankings, key=lambda r: (-r["alpha_score"], r["strategy"]))
    out = {"generated_at": datetime.utcnow().isoformat() + "Z", "rankings": rankings}
    target = save_path or RANK_DIR / "strategy_rankings.json"
    target.write_text(json.dumps(out, indent=2))
    return out
