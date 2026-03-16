from trace_invest.research.factor_library import (
    quality_factor,
    value_factor,
    growth_factor,
    momentum_factor,
    volatility_factor,
)
import json
from pathlib import Path


def test_quality_factor_missing():
    out = quality_factor("ABC", {}, {})
    assert out["factor_name"] == "quality"
    assert "value" in out
    assert out["value"] is None


def test_quality_factor_present():
    processed = {"financials": {"roe": 20}}
    out = quality_factor("ABC", processed, {})
    assert out["value"] == 20.0


def test_all_factors_return_schema():
    processed = {"financials": {"pe": 10, "roe": 15, "revenue_growth": 12}}
    hist = {"prices": [{"date": "2026-01-01", "close": 100}, {"date": "2026-01-02", "close": 105}], "rows": [{"conviction_score": 10}, {"conviction_score": 12}]}
    funcs = [value_factor, quality_factor, growth_factor, momentum_factor, volatility_factor]
    for f in funcs:
        out = f("TST", processed, hist)
        assert isinstance(out, dict)
        assert set(["symbol", "factor_name", "value", "metrics_used", "explanation"]).issubset(set(out.keys()))


def test_strategy_runner_creates_results():
    p = Path("data/strategies")
    assert p.exists()


def test_backtests_present():
    p = Path("data/backtests")
    assert p.exists()
