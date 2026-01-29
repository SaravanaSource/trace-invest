from typing import Dict


def compute_portfolio_valuation(
    portfolio: Dict,
    latest_prices: Dict[str, float]
) -> Dict:

    invested = 0
    unrealized_pnl = 0

    for symbol, pos in portfolio["positions"].items():
        price = latest_prices.get(symbol)
        if not price:
            continue

        current_value = pos["shares"] * price
        invested += current_value

        cost = pos["shares"] * pos["avg_price"]
        unrealized_pnl += current_value - cost

    total_equity = portfolio["cash"] + invested

    if portfolio["capital"] > 0:
        return_pct = round(
            (total_equity - portfolio["capital"])
            / portfolio["capital"] * 100,
            2
        )
    else:
        return_pct = None

    return {
        "capital": portfolio["capital"],
        "cash": round(portfolio["cash"], 2),
        "invested": round(invested, 2),
        "total_equity": round(total_equity, 2),
        "unrealized_pnl": round(unrealized_pnl, 2),
        "return_pct": return_pct
    }

