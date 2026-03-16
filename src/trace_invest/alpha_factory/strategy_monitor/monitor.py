import json
from pathlib import Path
from datetime import datetime
from statistics import mean, pstdev

DATA_DIR = Path(__file__).resolve().parents[3] / "data"
BACKTEST_DIR = DATA_DIR / "backtests"
MON_DIR = DATA_DIR / "strategy_monitoring"
MON_DIR.mkdir(parents=True, exist_ok=True)


def monitor_strategies(save_path: Path = None):
    reports = []
    for f in sorted(BACKTEST_DIR.glob("*.json")):
        data = json.loads(f.read_text())
        name = data.get("strategy_name") or f.stem
        monthly = data.get("monthly_returns") or data.get("returns") or []
        if not monthly:
            continue
        # rolling sharpe (12-month) - simple
        window = 12 if len(monthly) >= 12 else len(monthly)
        rolling_sharpe = None
        if window > 1:
            m = mean(monthly[-window:])
            s = pstdev(monthly[-window:]) if window > 1 else 0
            rolling_sharpe = (m / s * (12 ** 0.5)) if s > 0 else 0

        # drawdown trend: compare last 12 months cumulative vs previous 12 months
        def cum(r):
            c = 1.0
            for x in r:
                c *= (1 + x)
            return c - 1

        last12 = monthly[-12:]
        prev12 = monthly[-24:-12] if len(monthly) >= 24 else []
        trend = None
        if prev12 and last12:
            trend = cum(last12) - cum(prev12)

        report = {
            "strategy": name,
            "monthly_return_last": round(monthly[-1], 4) if monthly else None,
            "rolling_sharpe_12m": round(rolling_sharpe, 4) if rolling_sharpe is not None else None,
            "drawdown_trend_12m": round(trend, 4) if trend is not None else None,
        }
        reports.append(report)

    out = {"generated_at": datetime.utcnow().isoformat() + "Z", "monitoring": reports}
    target = save_path or MON_DIR / "strategy_monitoring.json"
    target.write_text(json.dumps(out, indent=2))
    return out
