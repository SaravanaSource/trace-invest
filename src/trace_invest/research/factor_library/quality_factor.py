from typing import Dict


def quality_factor(symbol: str, processed: Dict, history: Dict) -> Dict:
    """Compute a simple quality factor (ROE based).

    Expects `processed['financials']` to contain `roe` or `roe_ttm`.
    """
    fin = processed.get("financials", {}) or {}
    roe = fin.get("roe") or fin.get("roe_ttm")
    value = None
    explanation = "missing roe"
    try:
        if roe is not None:
            value = float(roe)
            explanation = f"ROE {value}"
    except Exception:
        explanation = "invalid roe"

    return {"factor_name": "quality_roe", "symbol": symbol, "factor_value": value, "explanation": explanation}

