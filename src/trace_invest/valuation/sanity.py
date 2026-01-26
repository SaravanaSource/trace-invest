from typing import Dict


def analyze_valuation_sanity(processed: Dict) -> Dict:
    valuation = processed.get("valuation_metrics") or {}

    pe = valuation.get("pe_ratio")
    pb = valuation.get("pb_ratio")
    fcf_yield = valuation.get("fcf_yield")

    bad = 0

    if pe is not None and pe > 40:
        bad += 1

    if pb is not None and pb > 8:
        bad += 1

    if fcf_yield is not None and fcf_yield < 0.02:
        bad += 1

    if bad == 0:
        return {
            "name": "valuation_sanity",
            "status": "REASONABLE",
            "risk": "LOW",
            "explanation": "Valuation within sane ranges",
        }

    if bad == 1:
        return {
            "name": "valuation_sanity",
            "status": "RICH",
            "risk": "MEDIUM",
            "explanation": "One valuation metric stretched",
        }

    return {
        "name": "valuation_sanity",
        "status": "EXPENSIVE",
        "risk": "HIGH",
        "explanation": "Multiple valuation metrics stretched",
    }

