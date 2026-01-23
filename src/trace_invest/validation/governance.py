from typing import Dict, List


def check_governance_flags(governance: Dict) -> Dict:
    """
    Governance and promoter risk checks.
    """

    flags: List[str] = []

    if governance.get("promoter_pledging_pct", 0) > 25:
        flags.append(
            "High promoter share pledging"
        )

    if governance.get("auditor_changes_last_5y", 0) >= 2:
        flags.append(
            "Frequent auditor changes"
        )

    if governance.get("independent_directors_pct", 100) < 33:
        flags.append(
            "Low independent director representation"
        )

    return {
        "layer": "governance",
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

