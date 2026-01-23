from typing import Dict


def valuation_score(metrics: Dict) -> Dict:
    """
    Scores valuation attractiveness (0–30).
    """

    score = 0
    reasons = []

    pe = metrics.get("pe_ratio", None)
    if pe is not None:
        if pe <= 15:
            score += 15
            reasons.append("Attractive PE")
        elif pe <= 25:
            score += 8
            reasons.append("Reasonable PE")

    pb = metrics.get("pb_ratio", None)
    if pb is not None and pb <= 3:
        score += 10
        reasons.append("Reasonable PB")

    fcf_yield = metrics.get("fcf_yield", 0)
    if fcf_yield >= 4:
        score += 5
        reasons.append("Healthy free cash flow yield")

    return {
        "component": "valuation",
        "score": min(score, 30),
        "max_score": 30,
        "reasons": reasons,
    }

