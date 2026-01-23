from typing import Dict

from trace_invest.validation.fraud import check_basic_fraud_flags
from trace_invest.validation.governance import check_governance_flags


def run_validation(processed_data: Dict) -> Dict:
    """
    Runs all fraud and governance checks.
    """

    fraud_result = check_basic_fraud_flags(
        processed_data.get("financials", {})
    )

    governance_result = check_governance_flags(
        processed_data.get("governance", {})
    )

    total_flags = fraud_result["flag_count"] + governance_result["flag_count"]

    return {
        "total_flags": total_flags,
        "overall_risk": _overall_risk(total_flags),
        "details": {
            "fraud": fraud_result,
            "governance": governance_result,
        },
    }


def _overall_risk(total_flags: int) -> str:
    if total_flags == 0:
        return "LOW"
    if total_flags <= 3:
        return "MEDIUM"
    return "HIGH"

