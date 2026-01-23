from typing import Dict


def quality_score(metrics: Dict) -> Dict:
    """
    Scores business quality (0–40).
    """

    score = 0
    reasons = []

    roe = metrics.get("roe", 0)
    if roe >= 15:
        score += 15
        reasons.append("Strong ROE")

    debt_to_equity = metrics.get("debt_to_equity", 1)
    if debt_to_equity <= 0.5:
        score += 10
        reasons.append("Low leverage")

    revenue_growth = metrics.get("revenue_growth_5y", 0)
    if revenue_growth >= 10:
        score += 10
        reasons.append("Consistent revenue growth")

    margins = metrics.get("operating_margin", 0)
    if margins >= 15:
        score += 5
        reasons.append("Healthy operating margins")

    return {
        "component": "quality",
        "score": min(score, 40),
        "max_score": 40,
        "reasons": reasons,
    }

