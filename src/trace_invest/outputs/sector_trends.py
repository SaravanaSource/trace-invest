from typing import Dict, List
from collections import defaultdict


def generate_sector_trends(decisions: List[Dict], universe: List[Dict]) -> Dict:

    symbol_to_sector = {
        s["symbol"]: s.get("sector", "UNKNOWN")
        for s in universe
    }

    buckets = defaultdict(list)

    for d in decisions:
        sector = symbol_to_sector.get(d.get("stock"), "UNKNOWN")
        trend = d.get("trend", {})
        delta = trend.get("delta")

        if delta is not None:
            buckets[sector].append(delta)

    output = {}

    for sector, deltas in buckets.items():

        if not deltas:
            avg = None
        else:
            avg = round(sum(deltas) / len(deltas), 2)

        if avg is None:
            label = "NO_DATA"
        elif avg >= 3:
            label = "IMPROVING"
        elif avg <= -3:
            label = "DETERIORATING"
        else:
            label = "STABLE"

        output[sector] = {
            "avg_trend_delta": avg,
            "trend": label,
            "count": len(deltas),
        }

    return output

