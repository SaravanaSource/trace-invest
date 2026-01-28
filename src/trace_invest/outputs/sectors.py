from typing import Dict, List
from collections import defaultdict


def generate_sector_summary(decisions: List[Dict], universe: List[Dict]) -> Dict:

    symbol_to_sector = {
        s["symbol"]: s.get("sector", "UNKNOWN")
        for s in universe
    }

    buckets = defaultdict(list)

    for d in decisions:
        sector = symbol_to_sector.get(d.get("stock"), "UNKNOWN")
        buckets[sector].append(d)

    output = {}

    for sector, rows in buckets.items():

        master_scores = []
        low_gov = 0
        strong_stab = 0

        for d in rows:
            v = d.get("validation", {})
            master = v.get("master", {})
            governance = v.get("governance", {})
            stability = v.get("stability", {})

            if master.get("master_score") is not None:
                master_scores.append(master.get("master_score"))

            if governance.get("governance_band") == "LOW":
                low_gov += 1

            if stability.get("stability_band") == "STRONG":
                strong_stab += 1

        count = len(rows)

        output[sector] = {
            "count": count,
            "avg_master_score": round(sum(master_scores) / len(master_scores), 1)
            if master_scores else None,
            "low_governance_pct": round(low_gov / count * 100, 1),
            "strong_stability_pct": round(strong_stab / count * 100, 1),
        }

    return output

