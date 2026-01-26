from typing import Dict, List
import statistics


def _extract_series(rows: List[Dict], keyword: str) -> Dict[str, float]:
    if not isinstance(rows, list):
        return {}

    for row in rows:
        if not isinstance(row, dict):
            continue

        name = str(row.get("index", "")).lower()

        if keyword in name:
            return {
                k: v
                for k, v in row.items()
                if k != "index"
            }

    return {}


def analyze_median_roe(processed: Dict) -> Dict:
    financials = processed.get("financials") or []

    series = _extract_series(financials, "roe")


    if not series:
        return {
            "name": "median_roe",
            "status": "NO_DATA",
            "risk": "UNKNOWN",
            "value": None,
            "explanation": "ROE history unavailable",
        }

    values = []

    for v in series.values():
        try:
            values.append(float(v))
        except Exception:
            continue

    if len(values) < 3:
        return {
            "name": "median_roe",
            "status": "INSUFFICIENT",
            "risk": "UNKNOWN",
            "value": None,
            "explanation": "Less than 3 years of ROE data",
        }

    median_roe = round(statistics.median(values), 2)

    if median_roe >= 0.18:
        status = "EXCELLENT"
        risk = "LOW"
    elif median_roe >= 0.12:
        status = "GOOD"
        risk = "LOW"
    elif median_roe >= 0.08:
        status = "AVERAGE"
        risk = "MEDIUM"
    else:
        status = "WEAK"
        risk = "HIGH"

    return {
        "name": "median_roe",
        "status": status,
        "risk": risk,
        "value": median_roe,
        "explanation": "5-year median return on equity",
    }

