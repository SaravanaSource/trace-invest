from datetime import datetime
from typing import Dict


def create_journal_entry(
    stock_name: str,
    signal: Dict,
) -> Dict:
    """
    Creates a snapshot-ready decision journal entry.
    """

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "stock": stock_name,
        "decision_zone": signal["zone"],
        "conviction_score": signal["conviction_score"],
        "overall_risk": signal["overall_risk"],
        "rationale": {
            "quality": signal["components"]["quality"]["reasons"],
            "valuation": signal["components"]["valuation"]["reasons"],
        },
    }

