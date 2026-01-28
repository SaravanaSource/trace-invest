from typing import Dict


def generate_narrative(decision: Dict) -> str:
    v = decision.get("validation", {})

    governance = v.get("governance", {})
    stability = v.get("stability", {})
    details = v.get("details", {})

    lines = []

    # --- Business Quality ---
    roe = details.get("median_roe", {})
    margin = details.get("median_operating_margin", {})

    if roe.get("status") in ("EXCELLENT", "GOOD"):
        lines.append("Business shows strong profitability.")
    elif roe.get("status") == "WEAK":
        lines.append("Business profitability is weak.")

    if margin.get("status") in ("EXCELLENT", "GOOD"):
        lines.append("Operating margins are healthy.")
    elif margin.get("status") == "WEAK":
        lines.append("Operating margins are thin.")

    # --- Governance ---
    gov_band = governance.get("governance_band")

    if gov_band == "LOW":
        lines.append("No major governance red flags detected.")
    elif gov_band == "MEDIUM":
        lines.append("Some governance concerns exist.")
    else:
        lines.append("High governance risk detected.")

    for risk in governance.get("top_risks", []):
        lines.append(f"Key issue: {risk.replace('_', ' ')}.")

    # --- Stability ---
    stab_band = stability.get("stability_band")

    if stab_band == "STRONG":
        lines.append("Business performance is stable across years.")
    elif stab_band == "AVERAGE":
        lines.append("Business shows mixed stability.")
    else:
        lines.append("Business shows unstable or weakening trends.")

    for weak in stability.get("weak_areas", []):
        lines.append(f"Weak area: {weak.replace('_', ' ')}.")

    # --- Valuation ---
    valuation = details.get("valuation_sanity", {})
    val_status = valuation.get("status")

    if val_status == "REASONABLE":
        lines.append("Valuation appears reasonable.")
    elif val_status == "RICH":
        lines.append("Valuation looks stretched.")
    elif val_status == "EXPENSIVE":
        lines.append("Valuation is expensive.")

    return " ".join(lines)

