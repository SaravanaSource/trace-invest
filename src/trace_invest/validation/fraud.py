from typing import Dict, List


def check_basic_fraud_flags(financials: Dict) -> Dict:
    """
    Basic fraud-related red flags.
    Input: normalized financial data (processed layer)
    Output: flags + explanations
    """

    flags: List[str] = []

    # Example checks (extend later)
    if financials.get("cash_flow_from_ops", 0) < 0 and financials.get("net_profit", 0) > 0:
        flags.append(
            "Net profit positive but operating cash flow negative"
        )

    if financials.get("receivables_growth_pct", 0) > 30:
        flags.append(
            "Receivables growing unusually fast"
        )

    if financials.get("related_party_txn_pct", 0) > 10:
        flags.append(
            "High related party transactions"
        )

    return {
        "layer": "fraud",
        "flag_count": len(flags),
        "flags": flags,
        "risk_level": _risk_level(len(flags)),
    }


def _risk_level(flag_count: int) -> str:
    if flag_count == 0:
        return "LOW"
    if flag_count <= 2:
        return "MEDIUM"
    return "HIGH"

