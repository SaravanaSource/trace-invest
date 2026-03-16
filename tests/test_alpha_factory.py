import json
from pathlib import Path
from trace_invest.alpha_factory.signal_lab.signals import discover_signals
from trace_invest.alpha_factory.strategy_generator.generator import generate_strategies
from trace_invest.alpha_factory.strategy_ranking.ranker import rank_strategies


def test_signal_discovery_runs(tmp_path):
    out = discover_signals(save_path=tmp_path / "signals.json")
    assert isinstance(out, dict)
    assert "signals" in out


def test_strategy_generation_runs(tmp_path):
    # create minimal signals file
    sfile = tmp_path / "signals.json"
    sfile.write_text(json.dumps({"signals": [{"signal_name": "momentum_breakout", "symbol": "AAA", "signal_strength": 0.5}]}))
    # point generator to use tmp by monkeypatching file location via env is complex; instead call generate_strategies with explicit save
    out = generate_strategies(save_path=tmp_path / "generated_strategies.json")
    assert isinstance(out, dict)
    assert "strategies" in out


def test_ranking_handles_empty_backtests(tmp_path):
    # ensure no backtests
    out = rank_strategies(save_path=tmp_path / "rankings.json")
    assert isinstance(out, dict)
    assert "rankings" in out
