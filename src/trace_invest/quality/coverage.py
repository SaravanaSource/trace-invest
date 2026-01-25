import math

def coverage_score(raw_fundamentals: dict, expected_years: int = 6) -> dict:
    """
    Computes coverage from raw Yahoo fundamentals.
    """

    years = set()

    for section in ["incomeStatementHistory", "balanceSheetHistory", "cashflowStatementHistory"]:
        rows = raw_fundamentals.get(section, [])

        for row in rows:
            for key, value in row.items():
                if not isinstance(key, str):
                    continue

                # keys like '2023-03-31'
                if key[:4].isdigit():
                    if value is None:
                        continue
                    if isinstance(value, float) and math.isnan(value):
                        continue

                    years.add(key[:4])

    available_years = len(years)
    ratio = round(available_years / expected_years, 2) if expected_years else 0.0

    return {
        "available_years": available_years,
        "expected_years": expected_years,
        "coverage_ratio": ratio,
        "years": sorted(years),
    }
