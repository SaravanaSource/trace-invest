from __future__ import annotations

from typing import Dict, List


def generate_market_summary(decisions: List[Dict], delta_stats: Dict) -> Dict:
    summary = {
        "total_stocks": len(decisions),
        "by_decision_zone": {},
        "by_overall_risk": {},
        "upgrades": delta_stats.get("upgrades", 0),
        "downgrades": delta_stats.get("downgrades", 0),
        "risk_increases": delta_stats.get("risk_increases", 0),
        "risk_decreases": delta_stats.get("risk_decreases", 0),
        "band_shifts": delta_stats.get("band_shifts", {}),
    }

    for decision in decisions:
        zone = decision.get("decision_zone")
        risk = decision.get("overall_risk")

        summary["by_decision_zone"][zone] = (
            summary["by_decision_zone"].get(zone, 0) + 1
        )

        summary["by_overall_risk"][risk] = (
            summary["by_overall_risk"].get(risk, 0) + 1
        )

    summary["market_tone"] = _market_tone(summary)
    return summary


def _market_tone(summary: Dict) -> str:
    total = summary.get("total_stocks", 0) or 0
    upgrades = summary.get("upgrades", 0)
    downgrades = summary.get("downgrades", 0)
    high_risk = summary.get("by_overall_risk", {}).get("HIGH", 0)

    if total == 0:
        return "NO_DATA"

    high_ratio = high_risk / total

    if upgrades > downgrades and high_ratio <= 0.2:
        return "CONSTRUCTIVE"
    if downgrades > upgrades or high_ratio >= 0.4:
        return "CAUTIOUS"
    return "MIXED"
