from typing import Dict, List


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


def analyze_balance_sheet_stress(processed: Dict) -> Dict:
    balance = processed.get("balance_sheet") or []
    financials = processed.get("financials") or []

    debt_series = _extract_series(balance, "total debt")
    ebitda_series = _extract_series(financials, "ebitda")

    if not debt_series or not ebitda_series:
        return {
            "name": "balance_sheet_stress",
            "status": "NO_DATA",
            "risk": "UNKNOWN",
            "explanation": "Debt or EBITDA data unavailable",
        }

    years = sorted(
        set(debt_series.keys()) & set(ebitda_series.keys()),
        reverse=True
    )

    if len(years) < 2:
        return {
            "name": "balance_sheet_stress",
            "status": "INSUFFICIENT",
            "risk": "UNKNOWN",
            "explanation": "Less than 2 years of overlapping data",
        }

    latest = years[0]
    oldest = years[-1]

    try:
        debt_change = float(debt_series[latest]) - float(debt_series[oldest])
        ebitda_change = float(ebitda_series[latest]) - float(ebitda_series[oldest])
    except Exception:
        return {
            "name": "balance_sheet_stress",
            "status": "ERROR",
            "risk": "UNKNOWN",
            "explanation": "Unable to compute changes",
        }

    if debt_change <= 0:
        return {
            "name": "balance_sheet_stress",
            "status": "STABLE",
            "risk": "LOW",
            "explanation": "Debt not increasing",
        }

    if debt_change > 0 and ebitda_change > 0:
        return {
            "name": "balance_sheet_stress",
            "status": "MANAGED",
            "risk": "MEDIUM",
            "explanation": "Debt rising but EBITDA also growing",
        }

    return {
        "name": "balance_sheet_stress",
        "status": "STRESSED",
        "risk": "HIGH",
        "explanation": "Debt rising while EBITDA not growing",
    }

