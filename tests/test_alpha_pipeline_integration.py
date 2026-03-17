import pytest
from trace_invest.alpha_factory.strategy_generator.generator import generate_strategies
from trace_invest.research.backtesting_engine.backtest import run_backtest


def test_generator_creates_strategies():
    g = generate_strategies(max_strategies=5)
    assert isinstance(g.get("strategies"), list)
    # expect at least one strategy given demo signals
    assert len(g.get("strategies")) >= 1


def test_backtester_runs_for_first_strategy():
    g = generate_strategies(max_strategies=3)
    if not g.get("strategies"):
        pytest.skip("no strategies generated")
    s = g.get("strategies")[0]
    res = run_backtest(s.get("strategy_name", "test"), s.get("positions", []))
    assert isinstance(res, dict)
    assert "CAGR" in res
