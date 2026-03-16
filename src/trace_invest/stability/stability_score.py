from typing import Dict

RISK_POINTS = {
    "LOW": 0,
    "MEDIUM": 2,
    "HIGH": 5,
    "UNKNOWN": 1,
}


def compute_stability_score(details: Dict) -> Dict:
    total = 0
    max_total = 0
    weak = []

    taxonomy = details.get("stability_taxonomy", {})
    taxonomy_status = taxonomy.get("status")

    for name, result in details.items():
        if not name.startswith(("median_", "revenue_cagr", "fcf_cagr", "consistency")):
            continue

        risk = result.get("risk", "UNKNOWN")
        points = RISK_POINTS.get(risk, 1)

        total += points
        max_total += 5

        if risk in ("HIGH", "MEDIUM"):
            weak.append(f"{name}:{result.get('status')}")

    if max_total == 0:
        score = 100
    else:
        score = round(100 - (total / max_total) * 100)

    # Taxonomy override: only structural decline should force WEAK.
    if taxonomy_status == "STRUCTURAL_DECLINE":
        weak.append("stability_taxonomy:STRUCTURAL_DECLINE")
        score = min(score, 49)
    elif taxonomy_status in ("STABLE_LOW_GROWTH", "CYCLICAL"):
        score = max(score, 50)

    if score >= 75:
        band = "STRONG"
    elif score >= 50:
        band = "AVERAGE"
    else:
        band = "WEAK"

    return {
        "stability_score": score,
        "stability_band": band,
        "weak_areas": weak,
    }

