from typing import Dict


def conviction_to_zone(conviction_score: int) -> str:
    if conviction_score >= 75:
        return "BUY"
    if conviction_score >= 55:
        return "HOLD"
    if conviction_score >= 35:
        return "REDUCE"
    return "EXIT"


def generate_signal(conviction_result: Dict) -> Dict:
    score = conviction_result["conviction_score"]
    zone = conviction_to_zone(score)

    return {
        "conviction_score": score,
        "zone": zone,
        "overall_risk": conviction_result["overall_risk"],
        "components": conviction_result["components"],
        "risk_penalty": conviction_result["risk_penalty"],
    }

