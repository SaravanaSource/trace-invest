from typing import Dict, List

MISSING_STATUSES = {
    "NO_DATA",
    "UNKNOWN",
    "INSUFFICIENT",
    "ERROR",
    "INVALID",
}

DECLINING_STATUSES = {
    "DECLINING",
    "STRUCTURAL_DECLINE",
}

HIGH_RISK_STATUSES = {
    "STRESSED",
    "PERSISTENT",
}


def build_system_awareness(decision: Dict, validation: Dict) -> Dict:
    details = validation.get("details", {})

    missing_inputs = _missing_inputs(details)
    weak_signals = _weak_signals(details)

    # Confidence only reflects data completeness, not the verdict itself.
    confidence_level = _confidence_level(len(missing_inputs))
    assessment_quality = _assessment_quality(len(missing_inputs))
    explanation = _explanation(missing_inputs, weak_signals, confidence_level)

    return {
        "confidence_level": confidence_level,
        "missing_inputs": missing_inputs,
        "weak_signals": weak_signals,
        "assessment_quality": assessment_quality,
        "explanation": explanation,
    }


def _missing_inputs(details: Dict) -> List[str]:
    missing = []

    for name, detail in details.items():
        status = detail.get("status")
        risk = detail.get("risk") or detail.get("risk_level")

        if status in MISSING_STATUSES or risk == "UNKNOWN":
            missing.append(name)

    return sorted(set(missing))


def _weak_signals(details: Dict) -> List[str]:
    weak = []

    for name, detail in details.items():
        status = detail.get("status")
        risk = detail.get("risk") or detail.get("risk_level")

        # High-risk or declining signals are surfaced for transparency.
        if risk == "HIGH":
            weak.append(f"{name}:{status}")
            continue

        if status in DECLINING_STATUSES or status in HIGH_RISK_STATUSES:
            weak.append(f"{name}:{status}")

    return sorted(set(weak))


def _confidence_level(missing_count: int) -> str:
    if missing_count >= 3:
        return "LOW"
    if missing_count >= 1:
        return "MEDIUM"
    return "HIGH"


def _assessment_quality(missing_count: int) -> str:
    if missing_count == 0:
        return "FINAL"
    if missing_count <= 2:
        return "PROVISIONAL"
    return "FRAGILE"


def _explanation(missing_inputs: List[str], weak_signals: List[str], confidence_level: str) -> str:
    if not missing_inputs:
        if weak_signals:
            return (
                "All critical data is present, but high-risk signals were detected; "
                "treat the verdict with caution."
            )
        return "All critical data is present; the verdict reflects full coverage."

    missing_summary = ", ".join(missing_inputs[:5])
    if len(missing_inputs) > 5:
        missing_summary += " (and others)"

    return (
        f"Confidence is {confidence_level} because key inputs are missing: {missing_summary}. "
        "Treat the verdict as provisional."
    )
