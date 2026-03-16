from typing import Dict, Any, List


def momentum_factor(symbol: str, processed: Dict[str, Any], history: Dict[str, Any] = None) -> Dict[str, Any]:
    """Canonical momentum factor.

    Prefer price-based momentum if `history['prices']` is present, otherwise use conviction delta.
    """
    metrics: List[str] = []

    # price-based momentum
    try:
        prices = (history or {}).get("prices", []) if isinstance(history, dict) else []
        if len(prices) >= 2:
            last = float(prices[-1]["close"])
            prev = float(prices[-2]["close"])
            if prev != 0:
                val = round((last / prev - 1.0) * 100.0, 4)
                metrics.append("prices")
                return {
                    "symbol": symbol,
                    "factor_name": "momentum",
                    "value": val,
                    "metrics_used": metrics,
                    "explanation": f"momentum_pct={val}",
                }
    except Exception:
        pass

    # fallback: conviction score delta
    try:
        rows = (history or {}).get("rows", []) if isinstance(history, dict) else []
        if len(rows) >= 2:
            last = float(rows[-1].get("conviction_score") or 0)
            prev = float(rows[-2].get("conviction_score") or 0)
            delta = round(last - prev, 4)
            metrics.append("conviction_rows")
            return {
                "symbol": symbol,
                "factor_name": "momentum",
                "value": delta,
                "metrics_used": metrics,
                "explanation": f"conviction_delta={delta}",
            }
    except Exception:
        pass

    return {
        "symbol": symbol,
        "factor_name": "momentum",
        "value": None,
        "metrics_used": metrics,
        "explanation": "insufficient history",
    }
