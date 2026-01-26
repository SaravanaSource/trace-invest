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


def analyze_capital_allocation(processed: Dict) -> Dict:
    cashflows = processed.get("cashflow") or []

    fcf_series = _extract_series(cashflows, "free cash flow")
    debt_repay_series = _extract_series(cashflows, "repayment")

    if not fcf_series:
        return {
            "name": "capital_allocation",
            "status": "NO_DATA",
            "risk": "UNKNOWN",
            "explanation": "Free cash flow data unavailable",
        }

    years = sorted(fcf_series.keys(), reverse=True)

    bad_years = 0

    for y in years:
        try:
            fcf = float(fcf_series.get(y, 0))
            repay = float(debt_repay_series.get(y, 0)) if debt_repay_series else 0
        except Exception:
            continue

        # repayment usually negative when paying debt
        if fcf > 0 and repay > 0:
            bad_years += 1

    if bad_years == 0:
        return {
            "name": "capital_allocation",
            "status": "DISCIPLINED",
            "risk": "LOW",
            "explanation": "Positive FCF not accompanied by rising debt",
        }

    if bad_years == 1:
        return {
            "name": "capital_allocation",
            "status": "QUESTIONABLE",
            "risk": "MEDIUM",
            "explanation": "One year of positive FCF with rising debt",
        }

    return {
        "name": "capital_allocation",
        "status": "POOR",
        "risk": "HIGH",
        "explanation": f"Positive FCF with rising debt in {bad_years} years",
    }

