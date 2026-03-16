from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

SNAPSHOT_VERSION = "v1"

GOVERNANCE_KEYS = {
    "earnings_quality",
    "unusual_items",
    "tax_volatility",
    "capital_allocation",
    "balance_sheet_stress",
}

STABILITY_KEYS = {
    "median_roe",
    "median_operating_margin",
    "revenue_cagr",
    "fcf_cagr",
    "consistency",
}

VALUATION_KEYS = {
    "valuation_sanity",
}

FRAUD_KEYS = {
    "fraud",
}


def build_reasoning_story(decision: Dict, snapshot_meta: Dict) -> Dict:
    validation = decision.get("validation", {})
    details = validation.get("details", {})

    facts = _group_facts(details)
    interpretation = _interpretation_rules(decision, validation)
    aggregation = _aggregation_logic(decision, validation)
    delta = _delta_interpretation(decision.get("delta", {}))
    verdict = _final_verdict(decision, validation)

    return {
        "metadata": {
            "stock": decision.get("stock"),
            "symbol": decision.get("symbol"),
            "run_date": snapshot_meta.get("run_date"),
            "snapshot_version": snapshot_meta.get("schema_version", SNAPSHOT_VERSION),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        },
        "evaluation_scope": {
            "categories": [
                "governance",
                "stability",
                "valuation",
                "fraud",
            ]
        },
        "observed_facts": facts,
        "interpretation_rules": interpretation,
        "aggregation_logic": aggregation,
        "delta_interpretation": delta,
        "final_verdict": verdict,
        "verification_guidance": _verification_guidance(),
    }


def reasoning_story_filename(decision: Dict) -> str:
    symbol = decision.get("symbol")
    if symbol:
        base = symbol.replace(".", "_")
    else:
        base = str(decision.get("stock") or "UNKNOWN").replace(" ", "_")

    cleaned = "".join(ch for ch in base.upper() if ch.isalnum() or ch == "_")
    return f"{cleaned}.json"


def _group_facts(details: Dict) -> Dict:
    grouped = {
        "governance": [],
        "stability": [],
        "valuation": [],
        "fraud": [],
        "other": [],
    }

    for key, value in details.items():
        fact = _fact_from_detail(key, value)
        if key in GOVERNANCE_KEYS:
            grouped["governance"].append(fact)
        elif key in STABILITY_KEYS:
            grouped["stability"].append(fact)
        elif key in VALUATION_KEYS:
            grouped["valuation"].append(fact)
        elif key in FRAUD_KEYS:
            grouped["fraud"].append(fact)
        else:
            grouped["other"].append(fact)

    return grouped


def _fact_from_detail(name: str, detail: Dict) -> Dict:
    return {
        "name": name,
        "status": detail.get("status"),
        "risk": detail.get("risk") or detail.get("risk_level"),
        "explanation": detail.get("explanation"),
    }


def _interpretation_rules(decision: Dict, validation: Dict) -> List[Dict]:
    governance = validation.get("governance", {})
    stability = validation.get("stability", {})
    master = validation.get("master", {})
    conviction_score = decision.get("conviction_score")
    overall_risk = validation.get("overall_risk")

    return [
        {
            "rule_id": "governance_band_thresholds",
            "statement": "Governance band is derived from governance score thresholds.",
            "inputs": {"governance_score": governance.get("governance_score")},
            "result": {"governance_band": governance.get("governance_band")},
        },
        {
            "rule_id": "stability_band_thresholds",
            "statement": "Stability band is derived from stability score thresholds.",
            "inputs": {"stability_score": stability.get("stability_score")},
            "result": {"stability_band": stability.get("stability_band")},
        },
        {
            "rule_id": "master_band_thresholds",
            "statement": "Master band aggregates governance, stability, and valuation sanity.",
            "inputs": {"master_score": master.get("master_score")},
            "result": {"master_band": master.get("master_band")},
        },
        {
            "rule_id": "overall_risk_from_flags",
            "statement": "Overall risk is derived from total flags across validation checks.",
            "inputs": {"total_flags": validation.get("total_flags")},
            "result": {"overall_risk": overall_risk},
        },
        {
            "rule_id": "decision_zone_from_conviction",
            "statement": "Decision zone is derived from conviction score thresholds.",
            "inputs": {"conviction_score": conviction_score},
            "result": {"decision_zone": decision.get("decision_zone")},
        },
    ]


def _aggregation_logic(decision: Dict, validation: Dict) -> Dict:
    governance = validation.get("governance", {})
    stability = validation.get("stability", {})
    master = validation.get("master", {})

    return {
        "governance_band": {
            "score": governance.get("governance_score"),
            "band": governance.get("governance_band"),
            "thresholds": {
                "LOW": ">= 75",
                "MEDIUM": ">= 50",
                "HIGH": "< 50",
            },
        },
        "stability_band": {
            "score": stability.get("stability_score"),
            "band": stability.get("stability_band"),
            "thresholds": {
                "STRONG": ">= 75",
                "AVERAGE": ">= 50",
                "WEAK": "< 50",
            },
        },
        "master_band": {
            "score": master.get("master_score"),
            "band": master.get("master_band"),
            "thresholds": {
                "ELITE": ">= 75",
                "GOOD": ">= 60",
                "AVERAGE": ">= 45",
                "POOR": "< 45",
            },
        },
        "overall_risk": {
            "total_flags": validation.get("total_flags"),
            "thresholds": {
                "LOW": "0",
                "MEDIUM": "1-3",
                "HIGH": ">= 4",
            },
        },
        "decision_zone": {
            "conviction_score": decision.get("conviction_score"),
            "thresholds": {
                "BUY": ">= 75",
                "HOLD": ">= 55",
                "REDUCE": ">= 35",
                "EXIT": "< 35",
            },
        },
    }


def _delta_interpretation(delta: Dict) -> Dict:
    decision_change = delta.get("decision_change")
    risk_change = delta.get("risk_change")

    impact = "NONE"
    if decision_change and decision_change != "UNCHANGED":
        impact = "VERDICT_CHANGED"
    elif risk_change and risk_change != "UNCHANGED":
        impact = "RISK_CHANGED"

    return {
        "change_summary": delta.get("change_summary"),
        "changes": delta.get("changes", []),
        "decision_change": decision_change,
        "risk_change": risk_change,
        "band_changes": delta.get("band_changes", {}),
        "verdict_impact": impact,
    }


def _final_verdict(decision: Dict, validation: Dict) -> Dict:
    governance = validation.get("governance", {})
    stability = validation.get("stability", {})
    valuation = validation.get("details", {}).get("valuation_sanity", {})

    reasons: List[str] = []
    for risk in governance.get("top_risks", [])[:3]:
        reasons.append(f"Governance issue: {risk}")

    for weak in stability.get("weak_areas", [])[:3]:
        reasons.append(f"Stability issue: {weak}")

    valuation_status = None
    if isinstance(valuation, dict):
        valuation_status = valuation.get("status")
    else:
        valuation_status = valuation

    if valuation_status and valuation_status != "REASONABLE":
        reasons.append(f"Valuation sanity: {valuation_status}")

    if not reasons:
        reasons.append("No material issues detected in rule checks")

    uncertainties = _uncertainties(validation.get("details", {}))

    return {
        "decision_zone": decision.get("decision_zone"),
        "overall_risk": decision.get("overall_risk"),
        "primary_reasons": reasons,
        "uncertainties": uncertainties,
    }


def _uncertainties(details: Dict) -> List[str]:
    items = []

    for name, detail in details.items():
        status = detail.get("status")
        risk = detail.get("risk") or detail.get("risk_level")
        if status in ("NO_DATA", "UNKNOWN") or risk in ("UNKNOWN", None):
            items.append(name)

    return sorted(set(items))


def _verification_guidance() -> List[str]:
    return [
        "Review multi-year income statements for revenue and margin trends.",
        "Verify operating cash flow aligns with reported profits.",
        "Check balance sheet leverage and debt movement over time.",
        "Inspect unusual or special items in the notes to accounts.",
        "Review tax rate history for volatility or anomalies.",
    ]
