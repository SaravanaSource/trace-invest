from typing import Dict


def compute_master_score(validation: Dict) -> Dict:
    governance = validation.get("governance", {})
    stability = validation.get("stability", {})
    valuation = validation.get("details", {}).get("valuation_sanity", {})

    g = governance.get("governance_score", 50)
    s = stability.get("stability_score", 50)

    v_risk = valuation.get("risk", "UNKNOWN")

    if v_risk == "LOW":
        v = 80
    elif v_risk == "MEDIUM":
        v = 60
    elif v_risk == "HIGH":
        v = 30
    else:
        v = 50

    score = round((g * 0.4) + (s * 0.4) + (v * 0.2))

    if score >= 75:
        band = "ELITE"
    elif score >= 60:
        band = "GOOD"
    elif score >= 45:
        band = "AVERAGE"
    else:
        band = "POOR"

    return {
        "master_score": score,
        "master_band": band,
    }

