from typing import Dict, List

def _extract_series(rows, target_keywords):
    """
    target_keywords: list of substrings to match against index name
    """
    if not isinstance(rows, list):
        return {}

    for row in rows:
        if not isinstance(row, dict):
            continue

        index_name = str(row.get("index", "")).lower()

        for kw in target_keywords:
            if kw.lower() in index_name:
                return {
                    k: v
                    for k, v in row.items()
                    if k != "index"
                }

    return {}




def analyze_earnings_quality(processed: Dict) -> Dict:
    financials = processed.get("financials") or []
    cashflows = processed.get("cashflow") or []

    net_income_series = _extract_series(
        financials,
        ["net income", "net profit"]
    )

    cfo_series = _extract_series(
        cashflows,
        [
            "operating cash flow",
            "cash from operating",
            "total cash from operating"
        ]
    )


    common_years = sorted(
        set(net_income_series.keys()) & set(cfo_series.keys()),
        reverse=True
    )

    if not common_years:
        return {
            "name": "earnings_quality",
            "status": "NO_DATA",
            "risk": "UNKNOWN",
            "explanation": "Net income or operating cash flow history unavailable",
        }

    negative_cfo_positive_profit_years = []

    for y in common_years:
        ni = net_income_series.get(y)
        cfo = cfo_series.get(y)

        if ni is None or cfo is None:
            continue

        if ni > 0 and cfo < 0:
            negative_cfo_positive_profit_years.append(y)

    count = len(negative_cfo_positive_profit_years)

    if count == 0:
        return {
            "name": "earnings_quality",
            "status": "CLEAN",
            "risk": "LOW",
            "explanation": "Operating cash flow aligns with profits",
        }

    if count == 1:
        return {
            "name": "earnings_quality",
            "status": "MINOR_MISMATCH",
            "risk": "MEDIUM",
            "explanation": "One year of positive profit but negative operating cash flow",
        }

    return {
        "name": "earnings_quality",
        "status": "REPEATED_MISMATCH",
        "risk": "HIGH",
        "explanation": f"Profit positive but operating cash flow negative in {count} years",
    }

