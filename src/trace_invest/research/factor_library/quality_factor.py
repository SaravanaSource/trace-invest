from typing import Dict, Any, List


def quality_factor(symbol: str, processed: Dict[str, Any], history: Dict[str, Any] = None) -> Dict[str, Any]:
    """Canonical quality factor based on ROE.

    Returns canonical schema: symbol, factor_name, value, metrics_used, explanation
    """
    fin = (processed or {}).get("financials", {}) or {}
    metrics: List[str] = []
    roe = None
    for k in ("roe", "roe_ttm", "roe_pct"):
        if k in fin:
            try:
                roe = float(fin[k])
                metrics.append(k)
                break
            except Exception:
                continue

    if roe is None:
        return {
            "symbol": symbol,
            "factor_name": "quality",
            "value": None,
            "metrics_used": metrics,
            "explanation": "missing roe",
        }

    return {
        "symbol": symbol,
        "factor_name": "quality",
        "value": round(roe, 4),
        "metrics_used": metrics,
        "explanation": f"ROE={roe}",
    }

