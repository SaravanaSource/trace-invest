from typing import Dict


def growth_factor(symbol: str, processed: Dict, history: Dict) -> Dict:
    """Simple growth factor using revenue growth fields.
    Expects `processed['financials']['revenue_ttm']` and `revenue_prev_ttm`.
    """
    fin = processed.get("financials", {}) or {}
    rev = fin.get("revenue_ttm")
    prev = fin.get("revenue_prev_ttm") or fin.get("revenue_prev")
    value = None
    explanation = "missing revenue"
    try:
        if rev is not None and prev is not None and float(prev) != 0:
            value = round((float(rev) / float(prev) - 1.0) * 100, 2)
            explanation = f"revenue growth {value}%"
    except Exception:
        explanation = "invalid revenue fields"

    return {"factor_name": "growth_revenue_pct", "symbol": symbol, "factor_value": value, "explanation": explanation}
from typing import Dict


def growth_factor(symbol: str, financials: Dict) -> Dict:
    # proxy: revenue growth
    growth = 0.0
    for k in ("revenue_growth", "revenue_growth_ttm", "revenue_cagr"):
        if k in financials:
            try:
                growth = float(financials[k])
                break
            except Exception:
                continue

    return {"factor_name": "growth", "symbol": symbol, "factor_value": growth, "explanation": f"revenue_growth={growth}"}
