from typing import List, Dict


def _top_n(items: List[Dict], key: str, n=30, reverse=True):
    return sorted(
        items,
        key=lambda x: x.get(key, 0),
        reverse=reverse
    )[:n]


def generate_rankings(decisions: List[Dict]) -> Dict:

    rows = []

    for d in decisions:
        v = d.get("validation", {})
        master = v.get("master", {})
        governance = v.get("governance", {})
        stability = v.get("stability", {})
        trend = d.get("trend", {})

        rows.append({
            "symbol": d.get("stock"),
            "master_score": master.get("master_score", 0),
            "master_band": master.get("master_band"),
            "governance_band": governance.get("governance_band"),
            "stability_band": stability.get("stability_band"),
            "trend": trend.get("trend"),
            "trend_delta": trend.get("delta"),
        })

    return {
        "top_master": _top_n(rows, "master_score", 30, True),
        "bottom_master": _top_n(rows, "master_score", 30, False),
        "low_governance": [r for r in rows if r["governance_band"] == "LOW"][:30],
        "strong_stability": [r for r in rows if r["stability_band"] == "STRONG"][:30],
        "top_improving": [
            r for r in rows if r["trend"] == "IMPROVING"
        ][:30],
        "top_deteriorating": [
            r for r in rows if r["trend"] == "DETERIORATING"
        ][:30],
    }

