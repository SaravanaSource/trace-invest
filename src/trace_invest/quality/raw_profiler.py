from typing import Dict


def profile_raw_fundamentals(raw: Dict) -> Dict:
    """
    High-level visibility of what blocks exist in raw fundamentals.
    """

    profile = {}

    profile["top_level_keys"] = list(raw.keys())

    info = raw.get("info", {})
    if isinstance(info, dict):
        profile["info_keys"] = list(info.keys())
    else:
        profile["info_keys"] = []

    profile["has_governance_block"] = "governance" in raw

    return profile

