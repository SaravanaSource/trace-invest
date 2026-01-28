from typing import Dict

RISK_POINTS = {
    "LOW": 0,
    "MEDIUM": 2,
    "HIGH": 5,
    "UNKNOWN": 1,
}


def compute_governance_score(details: Dict) -> Dict:
    total = 0
    max_total = 0
    risks = []

    for name, result in details.items():
        if name in ("fraud",):
            continue

        risk = result.get("risk", "UNKNOWN")
        points = RISK_POINTS.get(risk, 1)

        total += points
        max_total += 5

        if risk in ("HIGH", "MEDIUM"):
            risks.append(f"{name}:{result.get('status')}")

    if max_total == 0:
        score = 100
    else:
        score = round(100 - (total / max_total) * 100)

    if score >= 75:
        band = "LOW"
    elif score >= 50:
        band = "MEDIUM"
    else:
        band = "HIGH"

    return {
        "governance_score": score,
        "governance_band": band,
        "top_risks": risks,
    }

