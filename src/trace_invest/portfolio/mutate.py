from typing import Dict


def apply_portfolio_action(
    portfolio: Dict,
    action: Dict,
    last_price: float
) -> Dict:

    symbol = action.get("symbol")
    act = action.get("action")
    amount = action.get("amount", 0)

    if act == "BUY":
        shares = amount / last_price

        portfolio["cash"] -= amount

        portfolio["positions"][symbol] = {
            "shares": round(shares, 4),
            "avg_price": round(last_price, 2),
            "value": round(amount, 2)
        }

    elif act == "SELL":
        pos = portfolio["positions"].get(symbol)
        if pos:
            portfolio["cash"] += pos["value"]
            del portfolio["positions"][symbol]

    return portfolio

