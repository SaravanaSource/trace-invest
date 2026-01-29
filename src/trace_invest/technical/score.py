from typing import Dict


def compute_technical_score(technical: Dict, momentum: Dict) -> Dict:

    score = 0

    trend = technical.get("trend")
    mom = momentum.get("momentum")

    # Trend contribution
    if trend == "UP":
        score += 50
    elif trend == "SIDEWAYS":
        score += 25

    # Momentum contribution
    if mom == "POSITIVE":
        score += 50
    elif mom == "MIXED":
        score += 25

    if score >= 70:
        band = "STRONG"
    elif score >= 40:
        band = "NEUTRAL"
    else:
        band = "WEAK"

    return {
        "technical_score": score,
        "technical_band": band,
    }

