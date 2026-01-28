from typing import Dict, List
import statistics


def _extract_series(rows: List[Dict], keyword: str) -> Dict[str, float]:
    if not isinstance(rows, list):
        return {}

    for row in rows:
        if not isinstance(row, dict):
            continue

        name = str(row.get("index", "")).lower()

        if keyword in name or keyword.replace("_", " ") in name:
            return {
                k: v
                for k, v in row.items()
                if k != "index"
            }

    return {}


def analyze_median_operating_margin(processed: Dict) -> Dict:
    financials = processed.get("financials") or []

    series = _extract_series(financials, "operating margin")

    if not series:
        return {
            "name": "median_operating_margin",
            "status": "NO_DATA",
            "risk": "UNKNOWN",
            "value": None,
            "explanation": "Operating margin history unavailable",
        }

    values = []

    for v in series.values():
        try:
            values.append(float(v))
        except Exception:
            continue

    if len(values) < 3:
        return {
            "name": "median_operating_margin",
            "status": "INSUFFICIENT",
            "risk": "UNKNOWN",
            "value": None,
            "explanation": "Less than 3 years of operating margin data",
        }

    median_margin = round(statistics.median(values), 2)

    if median_margin >= 0.25:
        status = "EXCELLENT"
        risk = "LOW"
    elif median_margin >= 0.15:
        status = "GOOD"
        risk = "LOW"
    elif median_margin >= 0.08:
        status = "AVERAGE"
        risk = "MEDIUM"
    else:
        status = "WEAK"
        risk = "HIGH"

    return {
        "name": "median_operating_margin",
        "status": status,
        "risk": risk,
        "value": median_margin,
        "explanation": "5-year median operating margin",
    }

