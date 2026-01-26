from typing import Dict

from trace_invest.validation.fraud import check_basic_fraud_flags
from trace_invest.validation.registry import GOVERNANCE_ENGINES


def run_validation(processed: Dict) -> Dict:
    """
    Runs all validation engines.
    """

    fraud_result = check_basic_fraud_flags(
        processed.get("financials", {})
    )

    details = {
        "fraud": fraud_result
    }

    total_flags = fraud_result["flag_count"]

    for engine in GOVERNANCE_ENGINES:
        result = engine(processed)
        details[result["name"]] = result

        if result.get("risk") == "HIGH":
            total_flags += 1

    return {
        "total_flags": total_flags,
        "overall_risk": _overall_risk(total_flags),
        "details": details,
    }


def _overall_risk(total_flags: int) -> str:
    if total_flags == 0:
        return "LOW"
    if total_flags <= 3:
        return "MEDIUM"
    return "HIGH"
