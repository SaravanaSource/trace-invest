import json
from pathlib import Path

PORTFOLIO_PATH = Path("data/portfolio.json")


def load_portfolio():
    if not PORTFOLIO_PATH.exists():
        return {
            "capital": 0,
            "cash": 0,
            "positions": {}
        }
    return json.loads(PORTFOLIO_PATH.read_text())


def save_portfolio(portfolio):
    PORTFOLIO_PATH.write_text(
        json.dumps(portfolio, indent=2)
    )

