def coverage_score(financials: dict, expected_years: int = 6) -> dict:
    """
    Computes data coverage based on non-null historical values.
    """
    available_years = 0

    for _, values in financials.items():
        if isinstance(values, dict):
            available_years = max(
                available_years,
                sum(v is not None for v in values.values())
            )

    ratio = available_years / expected_years if expected_years else 0

    return {
        "available_years": available_years,
        "expected_years": expected_years,
        "coverage_ratio": round(ratio, 2),
    }

