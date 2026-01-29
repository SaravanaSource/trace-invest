from typing import Dict


def evaluate_exit_override(decision: Dict) -> Dict:

    v = decision.get("validation", {})
    master = v.get("master", {})
    governance = v.get("governance", {})
    trend = decision.get("trend", {})
    tech = decision.get("technical_score", {})

    master_band = master.get("master_band")
    gov_band = governance.get("governance_band")
    trend_label = trend.get("trend")
    tech_band = tech.get("technical_band")

    should_exit = (
        master_band == "POOR"
        or gov_band == "HIGH"
        or (trend_label == "DETERIORATING" and tech_band == "WEAK")
    )

    return {
        "exit_override": should_exit,
        "reasons": {
            "master_band": master_band,
            "governance_band": gov_band,
            "trend": trend_label,
            "technical_band": tech_band
        }
    }

