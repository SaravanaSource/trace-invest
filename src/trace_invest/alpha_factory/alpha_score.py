"""Alpha scoring utilities.

Provides deterministic alpha scoring combining performance and risk.
"""
from math import isnan


def compute_alpha_score(sharpe: float, cagr: float, consistency: float, max_drawdown: float) -> float:
    # defensive defaults
    s = sharpe or 0.0
    c = cagr or 0.0
    cons = consistency or 0.0
    dd = max_drawdown or 0.0
    # drawdown penalty: negative value reduces score
    dd_pen = max(0.0, -dd)
    score = 0.4 * s + 0.3 * c + 0.2 * cons + 0.1 * dd_pen
    if isnan(score):
        return 0.0
    return score
