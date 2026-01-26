from typing import Dict


RISK_POINTS = {
    "LOW": 0,
    "MEDIUM": 2,
    "HIGH": 5,
    "UNKNOWN": 1,
}


def compute_governance_score(details: Dict) -> Dict:
    """
    details: validation["details"]
    """

    total_points = 0
    max_points = 0
    top_risks = []

    for name, result in details.items():
        if name == "fraud":
            continue

        risk = result.get("risk", "UNKNOWN")
        points = RISK_POINTS.get(risk, 1)

        total_points += points
        max_points += 5

        if risk in ("HIGH", "MEDIUM"):
            top_risks.append(
                f"{name}: {result.get('status')}"
            )

    if max_points == 0:
        score = 100
    else:
        score = round(
            100 - (total_points / max_points) * 100
        )

    if score >= 75:
        band = "LOW"
    elif score >= 50:
        band = "MEDIUM"
    else:
        band = "HIGH"

    return {
        "governance_score": score,
        "governance_band": band,
        "top_risks": top_risks,
    }

