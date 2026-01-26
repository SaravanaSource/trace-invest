from typing import List, Dict


def extract_promoter_pledge(processed: Dict) -> List[Dict]:
    gov = processed.get("governance", {})
    value = gov.get("promoter_pledge_pct")

    if value is None:
        return []

    return [
        {
            "date": "latest",
            "pledge_pct": float(value),
        }
    ]


def analyze_pledge_trend(history: List[Dict]) -> Dict:
    if len(history) == 0:
        return {
            "status": "NO_DATA",
            "risk": "UNKNOWN",
            "explanation": "Promoter pledging data not available",
        }

    if len(history) == 1:
        pct = history[0]["pledge_pct"]

        if pct == 0:
            return {
                "status": "NONE",
                "risk": "LOW",
                "explanation": "No promoter pledging",
            }

        if pct < 10:
            return {
                "status": "LOW",
                "risk": "MEDIUM",
                "explanation": "Promoter pledging present but low",
            }

        return {
            "status": "HIGH",
            "risk": "HIGH",
            "explanation": "High promoter pledging",
        }

    # future-proof: trend logic
    values = [h["pledge_pct"] for h in history]
    first = values[0]
    last = values[-1]

    if last > first:
        return {
            "status": "INCREASING",
            "risk": "HIGH",
            "explanation": "Promoter pledging increasing over time",
        }

    if last < first:
        return {
            "status": "DECREASING",
            "risk": "MEDIUM",
            "explanation": "Promoter pledging decreasing",
        }

    return {
        "status": "FLAT",
        "risk": "MEDIUM",
        "explanation": "Promoter pledging stable",
    }
