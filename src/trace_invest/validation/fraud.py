from typing import Dict, List


def check_basic_fraud_flags(financials: Dict) -> Dict:
    """
    Basic fraud-related red flags.
    Input: normalized financial data (processed layer)
    Output: flags + explanations
    """

    # Defensive: validation must never crash
    if not isinstance(financials, dict):
        return {
            "layer": "fraud",
            "flag_count": 0,
            "flags": [],
            "risk_level": _risk_level(0),
        }

    flags: List[str] = []

    cfo = financials.get("cash_flow_from_ops")
    profit = financials.get("net_profit")
    recv_growth = financials.get("receivables_growth_pct")
    rpt_pct = financials.get("related_party_txn_pct")

    if cfo is not None and profit is not None:
        if cfo < 0 and profit > 0:
            flags.append("Net profit positive but operating cash flow negative")

    if recv_growth is not None:
        if recv_growth > 30:
            flags.append("Receivables growing unusually fast")

    if rpt_pct is not None:
        if rpt_pct > 10:
            flags.append("High related party transactions")

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

