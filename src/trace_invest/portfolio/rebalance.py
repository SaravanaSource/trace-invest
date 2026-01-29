from typing import Dict, List


TARGET_PCT = 0.05
MAX_PCT = 0.10
MIN_PCT = 0.02


def compute_rebalance_actions(
    portfolio: Dict,
    latest_prices: Dict[str, float],
    decisions: List[Dict]
) -> List[Dict]:

    actions = []

    capital = portfolio["capital"]
    positions = portfolio["positions"]

    decision_map = {
        d["stock"]: d for d in decisions
    }

    for symbol, pos in positions.items():

        price = latest_prices.get(symbol)
        if not price:
            continue

        value = pos["shares"] * price
        pct = value / capital

        # -----------------------
        # TRIM OVERSIZED
        # -----------------------
        if pct > MAX_PCT:
            excess_value = value - capital * TARGET_PCT

            actions.append({
                "action": "TRIM",
                "symbol": symbol,
                "amount": round(excess_value)
            })

        # -----------------------
        # TOP UP UNDERSIZED
        # -----------------------
        if pct < MIN_PCT:
            d = decision_map.get(symbol)
            if not d:
                continue

            entry = d.get("entry_filter", {})
            if entry.get("entry_allowed"):
                needed = capital * TARGET_PCT - value

                actions.append({
                    "action": "ADD",
                    "symbol": symbol,
                    "amount": round(needed)
                })

    return actions

