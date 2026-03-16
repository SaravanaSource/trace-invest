from typing import Dict, Any, List


def growth_factor(symbol: str, processed: Dict[str, Any], history: Dict[str, Any] = None) -> Dict[str, Any]:
    """Canonical growth factor using revenue growth proxies.

    Returns canonical schema: symbol, factor_name, value, metrics_used, explanation
    """
    fin = (processed or {}).get("financials", {}) or {}
    metrics: List[str] = []
    growth = None
    for k in ("revenue_growth", "revenue_growth_ttm", "revenue_cagr"):
        if k in fin:
            try:
                growth = float(fin[k])
                metrics.append(k)
                break
            except Exception:
                continue

    # fallback compute from revenue_ttm and revenue_prev_ttm
    if growth is None:
        rev = fin.get("revenue_ttm")
        prev = fin.get("revenue_prev_ttm") or fin.get("revenue_prev")
        if rev is not None and prev is not None:
            try:
                growth = (float(rev) / float(prev) - 1.0) * 100.0
                metrics.extend(["revenue_ttm", "revenue_prev_ttm"])
            except Exception:
                growth = None

    if growth is None:
        return {
            "symbol": symbol,
            "factor_name": "growth",
            "value": None,
            "metrics_used": metrics,
            "explanation": "missing growth metrics",
        }

    return {
        "symbol": symbol,
        "factor_name": "growth",
        "value": round(growth, 4),
        "metrics_used": metrics,
        "explanation": f"growth_pct={round(growth,4)}",
    }
