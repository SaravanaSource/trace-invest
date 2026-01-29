from typing import List, Dict


def compute_price_trend(prices: List[Dict]) -> Dict:
    """
    prices: list of {date, close}
    """

    if not prices or len(prices) < 200:
        return {
            "trend": "NO_DATA",
            "ma50": None,
            "ma200": None,
        }

    closes = [p["close"] for p in prices]

    ma50 = sum(closes[-50:]) / 50
    ma200 = sum(closes[-200:]) / 200
    last_price = closes[-1]

    if last_price > ma50 > ma200:
        trend = "UP"
    elif last_price < ma50 < ma200:
        trend = "DOWN"
    else:
        trend = "SIDEWAYS"

    return {
        "trend": trend,
        "ma50": round(ma50, 2),
        "ma200": round(ma200, 2),
    }

