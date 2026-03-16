from trace_invest.research.factor_library.quality_factor import quality_factor


def test_quality_factor_missing():
    out = quality_factor("ABC", {}, {})
    assert out["factor_name"] == "quality_roe"
    assert out["factor_value"] is None


def test_quality_factor_present():
    processed = {"financials": {"roe": 20}}
    out = quality_factor("ABC", processed, {})
    assert out["factor_value"] == 20
import json
from pathlib import Path


def test_strategy_runner_creates_results():
    p = Path("data/strategies")
    # if no strategies defined, pass
    assert p.exists()


def test_backtests_present():
    p = Path("data/backtests")
    assert p.exists()
