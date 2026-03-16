import json
from pathlib import Path


def test_opportunities_file_exists():
    p = Path("data/signals/top_opportunities.json")
    assert p.exists(), "top_opportunities.json is missing"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert isinstance(data, list) or isinstance(data, dict), "opportunities payload invalid"


def test_portfolio_file_exists():
    p = Path("data/portfolio/portfolio.json")
    assert p.exists(), "portfolio.json is missing"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert "positions" in data, "portfolio missing positions"


def test_alerts_file_exists():
    p = Path("data/alerts/alerts.json")
    assert p.exists(), "alerts.json is missing"
    data = json.loads(p.read_text(encoding="utf-8"))
    assert isinstance(data, list), "alerts payload must be a list"
