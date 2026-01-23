from typing import Dict

from trace_invest.intelligence.quality import quality_score
from trace_invest.intelligence.valuation import valuation_score


def conviction_score(processed_data: Dict, validation_result: Dict) -> Dict:
    """
    Produces final conviction score (0–100),
    capped by fraud/governance risk.
    """

    quality = quality_score(processed_data.get("quality_metrics", {}))
    valuation = valuation_score(processed_data.get("valuation_metrics", {}))

    base_score = quality["score"] + valuation["score"]

    # Risk penalty
    risk = validation_result.get("overall_risk", "LOW")
    penalty = _risk_penalty(risk)

    final_score = max(base_score - penalty, 0)

    return {
        "conviction_score": final_score,
        "base_score": base_score,
        "risk_penalty": penalty,
        "overall_risk": risk,
        "components": {
            "quality": quality,
            "valuation": valuation,
        },
    }


def _risk_penalty(risk: str) -> int:
    if risk == "LOW":
        return 0
    if risk == "MEDIUM":
        return 10
    return 25

