from trace_invest.portfolio_engine.engine import build_portfolio


def test_build_portfolio_basic():
    decisions = [{"symbol": "AAA", "conviction_score": 80}, {"symbol": "BBB", "conviction_score": 60}]
    signals = {"AAA": [{"signal_strength": 10}], "BBB": [{"signal_strength": 5}]}

    pf = build_portfolio(decisions, signals, max_position=0.6)
    assert "positions" in pf
    assert pf["cash"] >= 0.0
    assert any(p["symbol"] == "AAA" for p in pf["positions"])
