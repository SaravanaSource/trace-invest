from typing import Dict


def momentum_factor(symbol: str, processed: Dict, history: Dict) -> Dict:
    """Compute simple momentum using last two price points in `history['prices']`.
    Expects `history` may contain `prices` as list of {'date','close'}.
    """
    value = None
    explanation = "insufficient price history"
    try:
        prices = history.get("prices", []) if isinstance(history, dict) else []
        if len(prices) >= 2:
            last = float(prices[-1]["close"])
            prev = float(prices[-2]["close"])
            if prev != 0:
                value = round((last / prev - 1.0) * 100, 2)
                explanation = f"momentum {value}%"
    except Exception:
        explanation = "error computing momentum"

    return {"factor_name": "momentum_pct", "symbol": symbol, "factor_value": value, "explanation": explanation}
from typing import Dict


def momentum_factor(symbol: str, financials: Dict, history: Dict = None) -> Dict:
    # simple proxy: recent conviction change
    change = 0.0
    if history and isinstance(history, dict):
        rows = history.get("rows", [])
        if len(rows) >= 2:
            try:
                last = float(rows[-1].get("conviction_score") or 0)
                prev = float(rows[-2].get("conviction_score") or 0)
                change = last - prev
            except Exception:
                change = 0.0

    return {"factor_name": "momentum", "symbol": symbol, "factor_value": change, "explanation": f"conviction_delta={change}"}
