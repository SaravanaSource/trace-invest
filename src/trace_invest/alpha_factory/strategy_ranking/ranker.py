import json
from pathlib import Path
from math import sqrt
from datetime import datetime

from trace_invest.config import data_path, ensure_data_dirs

ensure_data_dirs("backtests", "strategy_rankings")
DATA_DIR = Path(__file__).resolve().parents[3] / "data"
BACKTEST_DIR = data_path("backtests")
RANK_DIR = data_path("strategy_rankings")
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
        name = data.get("strategy") or data.get("strategy_name") or f.stem
        # prefer explicit metrics from backtester
        cagr = data.get("CAGR") or data.get("cagr")
        sharpe = data.get("sharpe_ratio") or data.get("sharpe")
        max_dd = data.get("max_drawdown") or data.get("max_dd") or data.get("max_drawdown", 0)
        vol = data.get("volatility") or data.get("vol") or 0.0

        # fallback: if monthly returns present, compute metrics
        if cagr is None and data.get("monthly_returns"):
            m = _metrics_from_returns(data.get("monthly_returns"))
            cagr = m.get("cagr")
            sharpe = m.get("sharpe")
            max_dd = m.get("max_dd")

        # normalize values
        cagr = float(cagr or 0)
        sharpe = float(sharpe or 0)
        max_dd = float(max_dd or 0)

        # simple alpha score composition using available metrics
        alpha = 100 * (0.4 * (sharpe) + 0.35 * cagr + 0.15 * max(0, -max_dd) + 0.1 * max(0, -vol))

        rankings.append({
            "strategy": name,
            "alpha_score": round(alpha, 2),
            "CAGR": round(cagr, 4),
            "sharpe": round(sharpe, 4),
            "max_drawdown": round(max_dd, 4),
            "volatility": round(float(vol or 0), 4),
        })

    # deterministic sort: by alpha_score desc then name
    rankings = sorted(rankings, key=lambda r: (-r["alpha_score"], r["strategy"]))
    out = {"generated_at": datetime.utcnow().isoformat() + "Z", "rankings": rankings}
    target = save_path or RANK_DIR / "strategy_rankings.json"
    target.write_text(json.dumps(out, indent=2))
    return out
