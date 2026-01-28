from typing import Dict

from trace_invest.validation.fraud import check_basic_fraud_flags
from trace_invest.validation.registry import GOVERNANCE_ENGINES
from trace_invest.stability.registry import STABILITY_ENGINES
from trace_invest.stability.stability_score import compute_stability_score
from trace_invest.valuation.registry import VALUATION_ENGINES
from trace_invest.intelligence.master_score import compute_master_score


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

    governance_summary = compute_governance_score(details)


    for engine in STABILITY_ENGINES:
        result = engine(processed)
        details[result["name"]] = result

        if result.get("risk") == "HIGH":
            total_flags += 1
    
    stability_summary = compute_stability_score(details)

  
    for engine in VALUATION_ENGINES:
        result = engine(processed)
        details[result["name"]] = result

        if result.get("risk") == "HIGH":
            total_flags += 1

    master = compute_master_score({
            "governance": governance_summary,
            "stability": stability_summary,
            "details": details,
        })

    return {
        "total_flags": total_flags,
        "overall_risk": _overall_risk(total_flags),
        "details": details,
        "stability": stability_summary,
        "master": master,
    }


def _overall_risk(total_flags: int) -> str:
    if total_flags == 0:
        return "LOW"
    if total_flags <= 3:
        return "MEDIUM"
    return "HIGH"
