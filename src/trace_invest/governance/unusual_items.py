from typing import Dict, List


UNUSUAL_KEYWORDS = [
    "unusual",
    "special",
    "write off",
    "write-off",
    "restructuring",
]


def _extract_unusual_rows(rows: List[Dict]) -> List[Dict]:
    if not isinstance(rows, list):
        return []

    matches = []

    for row in rows:
        if not isinstance(row, dict):
            continue

        name = str(row.get("index", "")).lower()

        for kw in UNUSUAL_KEYWORDS:
            if kw in name:
                matches.append(row)
                break

    return matches


def analyze_unusual_items(processed: Dict) -> Dict:
    financials = processed.get("financials") or []

    rows = _extract_unusual_rows(financials)

    if not rows:
        return {
            "name": "unusual_items",
            "status": "NONE",
            "risk": "LOW",
            "explanation": "No unusual or special items reported",
        }

    years_with_values = set()

    for row in rows:
        for k, v in row.items():
            if k == "index":
                continue

            try:
                if v and abs(float(v)) > 0:
                    years_with_values.add(k)
            except Exception:
                continue

    count = len(years_with_values)

    if count == 1:
        return {
            "name": "unusual_items",
            "status": "ONE_TIME",
            "risk": "MEDIUM",
            "explanation": "One year shows unusual/special items",
        }

    return {
        "name": "unusual_items",
        "status": "PERSISTENT",
        "risk": "HIGH",
        "explanation": f"Unusual/special items present in {count} years",
    }

