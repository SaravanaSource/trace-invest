from typing import List
import math


def sharpe_ratio(returns: List[float], rf: float = 0.0) -> float:
    if not returns:
        return 0.0
    avg = sum(returns) / len(returns)
    sd = math.sqrt(sum((r - avg) ** 2 for r in returns) / len(returns))
    if sd == 0:
        return 0.0
    # annualize assuming monthly returns
    return (avg * 12 - rf) / (sd * (12 ** 0.5))


def sortino_ratio(returns: List[float], rf: float = 0.0) -> float:
    if not returns:
        return 0.0
    avg = sum(returns) / len(returns)
    neg = [r for r in returns if r < 0]
    if not neg:
        return float('inf')
    sd_down = math.sqrt(sum((r - avg) ** 2 for r in neg) / len(neg))
    if sd_down == 0:
        return 0.0
    return (avg * 12 - rf) / (sd_down * (12 ** 0.5))


def max_drawdown_from_series(values: List[float]) -> float:
    peak = -1e9
    mdd = 0.0
    for v in values:
        if v > peak:
            peak = v
        if peak != 0:
            mdd = min(mdd, (v - peak) / peak)
    return mdd
