from typing import Dict, List


def validate_financials_schema(data: Dict) -> List[str]:
    """Return list of schema issues (empty if valid).

    Deterministic checks: presence of top-level keys and basic types.
    """
    issues = []
    if not isinstance(data, dict):
        issues.append("payload-not-dict")
        return issues

    if "symbol" not in data:
        issues.append("missing-symbol")

    fin = data.get("financials")
    if fin is None:
        issues.append("missing-financials")
    elif not isinstance(fin, dict):
        issues.append("financials-not-dict")

    # Check for a minimal set of historical fields if present
    sample = fin.get("income_statement") if isinstance(fin, dict) else None
    if sample is not None and not isinstance(sample, list):
        issues.append("income-statement-not-list")

    return issues
