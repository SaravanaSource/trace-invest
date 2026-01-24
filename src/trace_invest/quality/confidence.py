def confidence_band(coverage: dict, freshness: dict) -> str:
    if coverage["coverage_ratio"] >= 0.75 and freshness["freshness"] == "GOOD":
        return "HIGH"
    if coverage["coverage_ratio"] >= 0.5:
        return "MEDIUM"
    return "LOW"

