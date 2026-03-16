from typing import Dict

DATA_CONFIDENCE_START = 100
DATA_CONFIDENCE_PENALTY = 12
DATA_CONFIDENCE_MIN = 0
DATA_CONFIDENCE_MAX = 100

GOVERNANCE_METRICS = {
    "earnings_quality",
    "unusual_items",
    "tax_volatility",
    "capital_allocation",
    "balance_sheet_stress",
}

STABILITY_METRICS = {
    "median_roe",
    "median_operating_margin",
    "revenue_cagr",
    "fcf_cagr",
    "consistency",
    "stability_taxonomy",
}


def compute_data_confidence(details: Dict) -> Dict:
    score = DATA_CONFIDENCE_START
    missing = 0

    for name, detail in details.items():
        if name not in GOVERNANCE_METRICS and name not in STABILITY_METRICS:
            continue

        status = detail.get("status")
        risk = detail.get("risk") or detail.get("risk_level")

        if status in ("NO_DATA", "UNKNOWN") or risk == "UNKNOWN":
            missing += 1
            score -= DATA_CONFIDENCE_PENALTY

    score = max(DATA_CONFIDENCE_MIN, min(DATA_CONFIDENCE_MAX, score))

    if score >= 75:
        band = "HIGH"
    elif score >= 50:
        band = "MEDIUM"
    else:
        band = "LOW"

    return {
        "data_confidence_score": score,
        "data_confidence_band": band,
        "missing_metric_count": missing,
    }
