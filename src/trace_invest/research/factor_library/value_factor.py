from typing import Dict, Any, List


def value_factor(symbol: str, processed: Dict[str, Any], history: Dict[str, Any] = None) -> Dict[str, Any]:
    """Canonical value factor.

    Returns dict with keys: symbol, factor_name, value, metrics_used, explanation
    """
    fin = (processed or {}).get("financials", {}) or {}
    pe = None
    metrics: List[str] = []
    for k in ("pe", "pe_ratio", "pe_ttm"):
        if k in fin:
            try:
                pe = float(fin[k])
                metrics.append(k)
                break
            except Exception:
                continue

    if pe is None or pe == 0:
        return {
            "symbol": symbol,
            "factor_name": "value",
            "value": None,
            "metrics_used": metrics,
            "explanation": "missing/invalid pe",
        }

    val = round(1.0 / pe, 6)
    return {
        "symbol": symbol,
        "factor_name": "value",
        "value": val,
        "metrics_used": metrics,
        "explanation": f"invPE={val}",
    }
