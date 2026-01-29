from typing import Dict


MAX_POSITIONS = 15
BASE_POSITION_PCT = 0.05   # 5%
MAX_POSITION_PCT = 0.10    # 10%


def evaluate_portfolio_action(
    portfolio: Dict,
    decision: Dict
) -> Dict:

    symbol = decision.get("stock")
    entry_filter = decision.get("entry_filter", {})
    decision_zone = decision.get("decision_zone")

    capital = portfolio["capital"]
    cash = portfolio["cash"]
    positions = portfolio["positions"]

    target_position_value = capital * BASE_POSITION_PCT

    # -----------------------------
    # BUY LOGIC
    # -----------------------------
    if (
        decision_zone == "ACCUMULATE"
        and entry_filter.get("entry_allowed")
        and symbol not in positions
        and len(positions) < MAX_POSITIONS
        and cash >= target_position_value
    ):
        return {
            "action": "BUY",
            "symbol": symbol,
            "amount": round(target_position_value)
        }

    # -----------------------------
    # SELL LOGIC
    # -----------------------------
    if decision_zone == "EXIT" and symbol in positions:
        return {
            "action": "SELL",
            "symbol": symbol,
            "amount": positions[symbol]["value"]
        }

    return {
        "action": "HOLD",
        "symbol": symbol
    }

