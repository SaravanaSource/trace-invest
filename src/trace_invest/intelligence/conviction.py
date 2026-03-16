from typing import Dict

MASTER_POINTS = {
    "ELITE": 35,
    "GOOD": 25,
    "AVERAGE": 15,
    "POOR": 5,
}

GOVERNANCE_POINTS = {
    "LOW": 20,
    "MEDIUM": 10,
    "HIGH": 0,
}

STABILITY_POINTS = {
    "STRONG": 20,
    "AVERAGE": 10,
    "WEAK": 0,
}

VALUATION_POINTS = {
    "REASONABLE": 15,
    "RICH": 8,
    "EXPENSIVE": 0,
    "UNKNOWN": 5,
}

DATA_CONFIDENCE_WEIGHT = 0.1
CONVICTION_MIN = 0
CONVICTION_MAX = 100
CONVICTION_FLOOR = 35


def conviction_score(processed_data: Dict, validation_result: Dict) -> Dict:
    """
    Produces final conviction score (0–100) from banded metrics and data confidence.
    """

    master_band = validation_result.get("master", {}).get("master_band")
    governance_band = validation_result.get("governance", {}).get("governance_band")
    stability_band = validation_result.get("stability", {}).get("stability_band")
    valuation = validation_result.get("details", {}).get("valuation_sanity", {})
    valuation_status = valuation.get("status") if isinstance(valuation, dict) else valuation

    data_confidence_score = validation_result.get("data_confidence_score", 100)
    data_confidence_band = validation_result.get("data_confidence_band", "HIGH")

    master_points = MASTER_POINTS.get(master_band, 0)
    governance_points = GOVERNANCE_POINTS.get(governance_band, 0)
    stability_points = STABILITY_POINTS.get(stability_band, 0)
    valuation_points = VALUATION_POINTS.get(valuation_status, 0)
    confidence_points = round(data_confidence_score * DATA_CONFIDENCE_WEIGHT)

    base_score = (
        master_points
        + governance_points
        + stability_points
        + valuation_points
        + confidence_points
    )

    # Floor protects against over-penalizing when core bands are acceptable.
    if master_band in ("ELITE", "GOOD", "AVERAGE") and governance_band != "HIGH":
        base_score = max(base_score, CONVICTION_FLOOR)

    final_score = max(CONVICTION_MIN, min(CONVICTION_MAX, base_score))

    return {
        "conviction_score": final_score,
        "base_score": base_score,
        "risk_penalty": 0,
        "overall_risk": validation_result.get("overall_risk", "LOW"),
        "data_confidence_score": data_confidence_score,
        "data_confidence_band": data_confidence_band,
        "components": {
            "master_band": master_band,
            "governance_band": governance_band,
            "stability_band": stability_band,
            "valuation_sanity": valuation_status,
            "data_confidence_points": confidence_points,
        },
    }

