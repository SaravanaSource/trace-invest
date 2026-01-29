from typing import List, Dict


def compute_momentum(prices: List[Dict]) -> Dict:
    """
    prices: list of {date, close}
    Assumes chronological order
    """

    if not prices or len(prices) < 252:
        return {
            "return_6m": None,
            "return_12m": None,
            "momentum": "NO_DATA",
        }

    closes = [p["close"] for p in prices]

    last = closes[-1]
    m6 = closes[-126]   # approx 6 months
    m12 = closes[-252] # approx 12 months

    r6 = round((last - m6) / m6 * 100, 1)
    r12 = round((last - m12) / m12 * 100, 1)

    if r6 > 0 and r12 > 0:
        label = "POSITIVE"
    elif r6 < 0 and r12 < 0:
        label = "NEGATIVE"
    else:
        label = "MIXED"

    return {
        "return_6m": r6,
        "return_12m": r12,
        "momentum": label,
    }

