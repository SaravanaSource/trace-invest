from typing import Dict

EXPECTED_YEARS = 6


def coverage_score(processed: Dict) -> Dict:
    years = set()

    financials = processed.get("financials", [])

    if isinstance(financials, list):
        for row in financials:
            if isinstance(row, dict):
                for k in row.keys():
                    if k != "index":
                        years.add(k)

    years = sorted(years, reverse=True)
    available = len(years)

    return {
        "available_years": available,
        "expected_years": EXPECTED_YEARS,
        "coverage_ratio": round(available / EXPECTED_YEARS, 2)
        if EXPECTED_YEARS else 0,
        "years": years,
    }
