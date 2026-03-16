from __future__ import annotations

from typing import Dict, List, Optional, Tuple


ZONE_ORDER = {
    "BUY": 3,
    "HOLD": 2,
    "REDUCE": 1,
    "EXIT": 0,
}

RISK_ORDER = {
    "LOW": 0,
    "MEDIUM": 1,
    "HIGH": 2,
    "UNKNOWN": 1,
}

MASTER_ORDER = {
    "ELITE": 3,
    "GOOD": 2,
    "AVERAGE": 1,
    "POOR": 0,
}

GOVERNANCE_ORDER = {
    "LOW": 2,
    "MEDIUM": 1,
    "HIGH": 0,
}

STABILITY_ORDER = {
    "STRONG": 2,
    "AVERAGE": 1,
    "WEAK": 0,
}

VALUATION_ORDER = {
    "REASONABLE": 2,
    "RICH": 1,
    "EXPENSIVE": 0,
    "UNKNOWN": 1,
}


def build_snapshot_deltas(
    decisions: List[Dict],
    previous_snapshot: Optional[Dict],
) -> Tuple[List[Dict], Dict]:
    prev_map = {}
    if previous_snapshot:
        for prev in previous_snapshot.get("decisions", []):
            if isinstance(prev, dict) and prev.get("stock"):
                prev_map[prev["stock"]] = prev

    stats = {
        "upgrades": 0,
        "downgrades": 0,
        "decision_zone_changes": 0,
        "risk_increases": 0,
        "risk_decreases": 0,
        "band_shifts": {
            "master": {"improved": 0, "worsened": 0},
            "governance": {"improved": 0, "worsened": 0},
            "stability": {"improved": 0, "worsened": 0},
            "valuation": {"improved": 0, "worsened": 0},
        },
    }

    for decision in decisions:
        prev = prev_map.get(decision.get("stock"))
        delta = build_stock_delta(decision, prev)
        decision["delta"] = delta

        if delta.get("decision_change") == "UPGRADE":
            stats["upgrades"] += 1
        elif delta.get("decision_change") == "DOWNGRADE":
            stats["downgrades"] += 1

        if delta.get("decision_change") in ("UPGRADE", "DOWNGRADE"):
            stats["decision_zone_changes"] += 1

        if delta.get("risk_change") == "INCREASE":
            stats["risk_increases"] += 1
        elif delta.get("risk_change") == "DECREASE":
            stats["risk_decreases"] += 1

        for band_key in ("master", "governance", "stability", "valuation"):
            change = delta.get("band_changes", {}).get(band_key)
            if change == "IMPROVED":
                stats["band_shifts"][band_key]["improved"] += 1
            elif change == "WORSENED":
                stats["band_shifts"][band_key]["worsened"] += 1

    return decisions, stats


def build_stock_delta(current: Dict, previous: Optional[Dict]) -> Dict:
    if not previous:
        return {
            "from_previous": None,
            "changes": ["Initial snapshot"],
            "change_summary": "Initial snapshot",
            "decision_change": "UNCHANGED",
            "risk_change": "UNCHANGED",
            "band_changes": {},
        }

    changes: List[str] = []
    band_changes: Dict[str, str] = {}

    prev_zone = previous.get("decision_zone")
    curr_zone = current.get("decision_zone")
    decision_change = _compare_ordered(prev_zone, curr_zone, ZONE_ORDER)

    if prev_zone != curr_zone:
        changes.append(f"Decision zone changed from {prev_zone} to {curr_zone}.")

    prev_risk = previous.get("overall_risk")
    curr_risk = current.get("overall_risk")
    risk_change = _compare_ordered(prev_risk, curr_risk, RISK_ORDER)

    if prev_risk != curr_risk:
        verb = "increased" if risk_change == "INCREASE" else "decreased"
        changes.append(f"Overall risk {verb} from {prev_risk} to {curr_risk}.")

    changes, band_changes = _compare_band(
        changes,
        band_changes,
        "master",
        _nested(previous, ("master", "master_band")),
        _nested(current, ("master", "master_band")),
        MASTER_ORDER,
        "Master band",
    )

    changes, band_changes = _compare_band(
        changes,
        band_changes,
        "governance",
        _nested(previous, ("governance", "governance_band")),
        _nested(current, ("governance", "governance_band")),
        GOVERNANCE_ORDER,
        "Governance band",
    )

    changes, band_changes = _compare_band(
        changes,
        band_changes,
        "stability",
        _nested(previous, ("stability", "stability_band")),
        _nested(current, ("stability", "stability_band")),
        STABILITY_ORDER,
        "Stability band",
    )

    changes, band_changes = _compare_band(
        changes,
        band_changes,
        "valuation",
        _nested(previous, ("valuation", "valuation_sanity")),
        _nested(current, ("valuation", "valuation_sanity")),
        VALUATION_ORDER,
        "Valuation sanity",
    )

    if not changes:
        changes = ["No material changes"]

    return {
        "from_previous": {
            "decision_zone": prev_zone,
            "overall_risk": prev_risk,
            "master_band": _nested(previous, ("master", "master_band")),
            "governance_band": _nested(previous, ("governance", "governance_band")),
            "stability_band": _nested(previous, ("stability", "stability_band")),
            "valuation_sanity": _nested(previous, ("valuation", "valuation_sanity")),
        },
        "changes": changes,
        "change_summary": " ".join(changes),
        "decision_change": decision_change,
        "risk_change": risk_change,
        "band_changes": band_changes,
    }


def _compare_ordered(prev: Optional[str], curr: Optional[str], order: Dict[str, int]) -> str:
    prev_val = order.get(prev or "", 0)
    curr_val = order.get(curr or "", 0)

    if curr_val > prev_val:
        return "UPGRADE" if order is ZONE_ORDER else "INCREASE"
    if curr_val < prev_val:
        return "DOWNGRADE" if order is ZONE_ORDER else "DECREASE"
    return "UNCHANGED"


def _compare_band(
    changes: List[str],
    band_changes: Dict[str, str],
    key: str,
    prev: Optional[str],
    curr: Optional[str],
    order: Dict[str, int],
    label: str,
) -> Tuple[List[str], Dict[str, str]]:
    if prev == curr:
        return changes, band_changes

    prev_val = order.get(prev or "", 0)
    curr_val = order.get(curr or "", 0)

    if curr_val > prev_val:
        band_changes[key] = "IMPROVED"
        verb = "improved"
    else:
        band_changes[key] = "WORSENED"
        verb = "weakened"

    changes.append(f"{label} {verb} from {prev} to {curr}.")
    return changes, band_changes


def _nested(obj: Dict, path: Tuple[str, ...]) -> Optional[str]:
    current = obj
    for key in path:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current
