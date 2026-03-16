from typing import Dict
import math


def volatility_factor(symbol: str, processed: Dict, history: Dict) -> Dict:
    """Estimate volatility using recent daily returns in `history['prices']`.
    Returns annualized std dev percent if possible.
    """
    explanation = "insufficient price history"
    value = None
    try:
        prices = history.get("prices", []) if isinstance(history, dict) else []
        if len(prices) >= 3:
            closes = [float(p["close"]) for p in prices]
            returns = []
            for i in range(1, len(closes)):
                prev = closes[i-1]
                if prev != 0:
                    returns.append((closes[i] / prev) - 1.0)
            if returns:
                mean = sum(returns)/len(returns)
                var = sum((r-mean)**2 for r in returns)/len(returns)
                sd = math.sqrt(var)
                # annualize assuming weekly closes ~52 obs -> factor sqrt(52)
                annual = sd * (52**0.5)
                value = round(annual * 100, 2)
                explanation = f"annualized volatility {value}%"
    except Exception:
        explanation = "error computing volatility"

    return {"factor_name": "volatility_annual_pct", "symbol": symbol, "factor_value": value, "explanation": explanation}
from typing import Dict


def volatility_factor(symbol: str, financials: Dict, prices: list = None) -> Dict:
    # placeholder: return low volatility if no price history
    vol = 0.0
    if prices:
        try:
            # simple stddev proxy on returns
            returns = []
            for i in range(1, len(prices)):
                if prices[i-1] != 0:
                    returns.append((prices[i] - prices[i-1]) / prices[i-1])
            if returns:
                import math
                mean = sum(returns)/len(returns)
                var = sum((r-mean)**2 for r in returns)/len(returns)
                vol = math.sqrt(var)
        except Exception:
            vol = 0.0

    return {"factor_name": "volatility", "symbol": symbol, "factor_value": vol, "explanation": f"volatility={vol}"}
