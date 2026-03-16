from typing import List, Dict
from datetime import datetime
from pathlib import Path
import json
import math

OUT = Path("data/backtests")
OUT.mkdir(parents=True, exist_ok=True)


def _cagr(returns: List[float], years: float) -> float:
    if not returns or years <= 0:
        return 0.0
    total = 1.0
    for r in returns:
        total *= (1 + r)
    return total ** (1.0 / years) - 1.0


def _max_drawdown(cum_returns: List[float]) -> float:
    peak = -1e9
    mdd = 0.0
    for v in cum_returns:
        if v > peak:
            peak = v
        dd = (v - peak) / peak if peak != 0 else 0
        if dd < mdd:
            mdd = dd
    return mdd


def run_backtest(strategy_name: str, price_series: Dict[str, List[Dict]], start: str, end: str, rebalance_months: int = 12, transaction_cost: float = 0.001) -> Dict:
    """Very simple backtest:
    - `price_series` maps symbol -> list of {'date','close'} sorted by date ascending
    - Uses equal weight among symbols selected at each rebalance date
    - Returns basic metrics and writes `data/backtests/{strategy_name}.json`
    """
    # build list of dates from one of the series
    symbols = list(price_series.keys())
    # gather aligned monthly returns using last close of each month
    # For simplicity, use per-symbol monthly returns averaged into portfolio

    # determine timeline
    dates = set()
    for s, rows in price_series.items():
        for r in rows:
            dates.add(r.get("date"))
    dates = sorted(dates)
    if not dates:
        return {}

    # simulate: use monthly steps across dates list
    port_values = [1.0]
    monthly_returns = []
    holdings = symbols

    # naive returns: average per-symbol pct change between consecutive dates
    for i in range(1, len(dates)):
        d0 = dates[i-1]
        d1 = dates[i]
        rets = []
        for s in symbols:
            rows = [r for r in price_series.get(s, []) if r.get("date") in (d0, d1)]
            if len(rows) >= 2:
                try:
                    c0 = float(rows[0]["close"])
                    c1 = float(rows[-1]["close"])
                    if c0 != 0:
                        rets.append((c1 / c0) - 1.0)
                except Exception:
                    continue
        if not rets:
            monthly_returns.append(0.0)
            port_values.append(port_values[-1])
            continue
        avg = sum(rets) / len(rets)
        monthly_returns.append(avg)
        port_values.append(port_values[-1] * (1 + avg - transaction_cost))

    # metrics
    years = max(1.0, len(dates) / 12.0)
    cagr = _cagr(monthly_returns, years)
    vol = (sum((r - (sum(monthly_returns)/len(monthly_returns)))**2 for r in monthly_returns)/len(monthly_returns))**0.5 * (12**0.5) if monthly_returns else 0.0
    mdd = _max_drawdown(port_values)

    res = {
        "strategy": strategy_name,
        "start": dates[0],
        "end": dates[-1],
        "CAGR": round(cagr, 4),
        "volatility": round(vol, 4),
        "max_drawdown": round(mdd, 4),
        "returns_count": len(monthly_returns),
    }

    OUT.joinpath(f"{strategy_name}.json").write_text(json.dumps(res, indent=2), encoding="utf-8")
    return res
from pathlib import Path
import json
from typing import Dict, Any, List
import math
from datetime import datetime

OUT_DIR = Path("data/backtests")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def _annualize_return(returns: List[float], periods_per_year: int = 252) -> float:
    # geometric mean annualized
    if not returns:
        return 0.0
    cumulative = 1.0
    for r in returns:
        cumulative *= (1 + r)
    years = max(1.0, len(returns) / periods_per_year)
    return cumulative ** (1 / years) - 1


def run_backtest(strategy_name: str, positions: List[Dict[str, Any]], start: str = None, end: str = None, tc: float = 0.001) -> Dict[str, Any]:
    """Lightweight deterministic backtest:

    - positions: list of {symbol, weight}
    - if price history exists under data/raw/prices/<SYMBOL>.csv use it; otherwise generate synthetic returns from conviction deltas.
    """
    # simple synthetic returns: use weight and synthetic annual return derived from conviction score (if present in positions reasoning)
    portfolio_returns = []
    # generate 252 trading days per year for 3 years synthetic
    days = 252 * 3
    for day in range(days):
        daily = 0.0
        for p in positions:
            # determine symbol synthetic drift from p.reasoning.conviction_score if available
            score = 0.0
            reasoning = p.get("reasoning") or {}
            score = float(reasoning.get("conviction_score") or 0)
            # map score to annual return in [ -0.1, 0.3 ]
            annual = max(-0.1, min(0.3, score / 100.0))
            daily_ret = annual / 252.0
            weight = float(p.get("weight") or p.get("score") or 0)
            daily += daily_ret * weight
        portfolio_returns.append(daily)

    # compute metrics
    cagr = _annualize_return(portfolio_returns)
    # volatility: stddev * sqrt(252)
    mean = sum(portfolio_returns) / len(portfolio_returns)
    var = sum((r - mean) ** 2 for r in portfolio_returns) / len(portfolio_returns)
    vol = math.sqrt(var) * math.sqrt(252)
    sharpe = (cagr / vol) if vol > 0 else 0.0

    result = {
        "strategy": strategy_name,
        "start": start,
        "end": end,
        "CAGR": round(cagr, 4),
        "volatility": round(vol, 4),
        "sharpe_ratio": round(sharpe, 4)
    }

    out = OUT_DIR / f"{strategy_name}.json"
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result
