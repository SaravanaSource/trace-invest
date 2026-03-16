from typing import Dict


def value_factor(symbol: str, processed: Dict, history: Dict) -> Dict:
    """Simple value factor using inverse PE (higher is cheaper).
    Expects `processed['financials']['pe_ratio']`.
    """
    fin = processed.get("financials", {}) or {}
    pe = fin.get("pe_ratio") or fin.get("pe")
    value = None
    explanation = "missing pe"
    try:
        if pe is not None and float(pe) > 0:
            value = round(1.0 / float(pe), 6)
            explanation = f"invPE {value}"
    except Exception:
        explanation = "invalid pe"

    return {"factor_name": "value_inv_pe", "symbol": symbol, "factor_value": value, "explanation": explanation}
from typing import Dict


def value_factor(symbol: str, financials: Dict) -> Dict:
    pe = None
    for k in ("pe", "pe_ratio", "pe_ttm"):
        if k in financials:
            try:
                pe = float(financials[k])
                break
            except Exception:
                continue

    val = pe if pe is not None else 9999.0
    return {"factor_name": "value", "symbol": symbol, "factor_value": val, "explanation": f"PE={val}"}
