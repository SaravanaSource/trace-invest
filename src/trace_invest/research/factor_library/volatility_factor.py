from typing import Dict, Any, List
import math


def volatility_factor(symbol: str, processed: Dict[str, Any], history: Dict[str, Any] = None) -> Dict[str, Any]:
    """Canonical volatility factor returning annualized volatility percent.

    Returns canonical schema: symbol, factor_name, value, metrics_used, explanation
    """
    metrics: List[str] = []
    try:
        prices = (history or {}).get("prices", []) if isinstance(history, dict) else []
        if len(prices) >= 3:
            closes = [float(p["close"]) for p in prices]
            returns = []
            for i in range(1, len(closes)):
                prev = closes[i - 1]
                if prev != 0:
                    returns.append((closes[i] / prev) - 1.0)
            if returns:
                mean = sum(returns) / len(returns)
                var = sum((r - mean) ** 2 for r in returns) / len(returns)
                sd = math.sqrt(var)
                # annualize assuming typical ~252 trading days
                annual = sd * math.sqrt(252)
                val = round(annual * 100.0, 4)
                metrics.append("prices")
                return {
                    "symbol": symbol,
                    "factor_name": "volatility",
                    "value": val,
                    "metrics_used": metrics,
                    "explanation": f"annualized_vol_pct={val}",
                }
    except Exception:
        pass

    return {
        "symbol": symbol,
        "factor_name": "volatility",
        "value": None,
        "metrics_used": metrics,
        "explanation": "insufficient price history or error",
    }
