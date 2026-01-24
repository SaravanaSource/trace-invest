def coverage_score(processed: dict, expected_years: int = 6) -> dict:
    """
    Computes data coverage based on available fiscal years
    across financial statements.
    """

    years = set()

    for section in ["income_statement", "balance_sheet", "cashflow"]:
        rows = processed.get(section, [])
        for row in rows:
            for key in row.keys():
                if isinstance(key, str) and key[:4].isdigit():
                    years.add(key[:4])

    available_years = len(years)
    ratio = available_years / expected_years if expected_years else 0

    return {
        "available_years": available_years,
        "expected_years": expected_years,
        "coverage_ratio": round(ratio, 2),
        "years": sorted(years),
    }
