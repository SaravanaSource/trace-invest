from typing import Dict


def conviction_to_zone(conviction_score: int) -> str:
    """
    Map numeric conviction score (0-100) to human decision zones.

    Zones (deterministic):
    - STRONG_BUY: conviction >= 85
    - BUY: conviction >= 70
    - HOLD: conviction >= 55
    - CAUTION: conviction >= 40
    - AVOID: otherwise

    These thresholds are intentionally conservative and deterministic.
    """
    if conviction_score >= 85:
        return "STRONG_BUY"
    if conviction_score >= 70:
        return "BUY"
    if conviction_score >= 55:
        return "HOLD"
    if conviction_score >= 40:
        return "CAUTION"
    return "AVOID"


def generate_signal(conviction_result: Dict) -> Dict:
    score = conviction_result["conviction_score"]
    zone = conviction_to_zone(score)

    # If data confidence is low, avoid aggressive negative actions; prefer `HOLD`.
    if conviction_result.get("data_confidence_band") == "LOW" and zone in ("AVOID", "CAUTION"):
        zone = "HOLD"

    return {
        "conviction_score": score,
        "zone": zone,
        "overall_risk": conviction_result["overall_risk"],
        "components": conviction_result["components"],
        "risk_penalty": conviction_result["risk_penalty"],
    }

