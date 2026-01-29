from typing import Dict


def passes_entry_filter(decision: Dict) -> Dict:

    v = decision.get("validation", {})
    master = v.get("master", {})
    governance = v.get("governance", {})
    tech = decision.get("technical_score", {})

    master_band = master.get("master_band")
    gov_band = governance.get("governance_band")
    tech_band = tech.get("technical_band")

    allowed = (
        master_band in ("GOOD", "ELITE")
        and gov_band == "LOW"
        and tech_band == "STRONG"
    )

    return {
        "entry_allowed": allowed,
        "reason": {
            "master_band": master_band,
            "governance_band": gov_band,
            "technical_band": tech_band,
        }
    }

