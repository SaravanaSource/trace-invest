from typing import Dict, List
import math


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


def analyze_revenue_cagr(processed: Dict) -> Dict:
    financials = processed.get("financials") or []

    series = _extract_series(financials, "revenue")

    if not series:
        return {
            "name": "revenue_cagr",
            "status": "NO_DATA",
            "risk": "UNKNOWN",
            "value": None,
            "explanation": "Revenue history unavailable",
        }

    items = sorted(series.items())
    start_year, start_val = items[0]
    end_year, end_val = items[-1]

    try:
        start = float(start_val)
        end = float(end_val)
    except Exception:
        return {
            "name": "revenue_cagr",
            "status": "ERROR",
            "risk": "UNKNOWN",
            "value": None,
            "explanation": "Invalid revenue values",
        }

    if start <= 0 or end <= 0:
        return {
            "name": "revenue_cagr",
            "status": "INVALID",
            "risk": "UNKNOWN",
            "value": None,
            "explanation": "Non-positive revenue values",
        }

    years = max(len(items) - 1, 1)
    cagr = round((end / start) ** (1 / years) - 1, 3)

    if cagr >= 0.12:
        status = "STRONG"
        risk = "LOW"
    elif cagr >= 0.05:
        status = "MODERATE"
        risk = "LOW"
    elif cagr >= 0:
        status = "WEAK"
        risk = "MEDIUM"
    else:
        status = "DECLINING"
        risk = "HIGH"

    return {
        "name": "revenue_cagr",
        "status": status,
        "risk": risk,
        "value": cagr,
        "explanation": "Revenue compound annual growth rate",
    }

