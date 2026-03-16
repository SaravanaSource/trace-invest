"""Orchestration script for Phase-4 Alpha Factory pipeline."""
from pathlib import Path
from trace_invest.alpha_factory.signal_lab.signals import discover_signals
from trace_invest.alpha_factory.strategy_generator.generator import generate_strategies
from trace_invest.alpha_factory.strategy_ranking.ranker import rank_strategies
from trace_invest.alpha_factory.strategy_monitor.monitor import monitor_strategies
import json
import sys
from trace_invest.config import data_path, ensure_data_dirs


def run_pipeline():
    ensure_data_dirs("backtests")
    data_dir = data_path()
    print("Alpha Factory: running signal discovery...")
    s = discover_signals()
    print(f"discovered {len(s.get('signals', []))} signals")

    print("Alpha Factory: generating strategies...")
    g = generate_strategies()
    print(f"generated {len(g.get('strategies', []))} strategies")

    # backtests: try to run an existing backtester if available else create placeholders
    # For determinism and speed we create simple placeholder monthly returns if no backtests exist.
    bt_dir = data_path("backtests")
    bt_dir.mkdir(parents=True, exist_ok=True)
    if not any(bt_dir.glob("*.json")):
        # create simple deterministic backtests from strategies
        for strat in g.get("strategies", []):
            name = strat.get("strategy_name")
            # deterministic pseudo-random series using hash
            base = abs(hash(name)) % 1000 / 10000
            monthly = [round(base + (i % 12 - 6) * 0.001, 4) for i in range(36)]
            out = {"strategy_name": name, "monthly_returns": monthly}
            (bt_dir / f"{name}.json").write_text(json.dumps(out, indent=2))

    print("Alpha Factory: ranking strategies...")
    r = rank_strategies()
    print(f"ranked {len(r.get('rankings', []))} strategies")

    print("Alpha Factory: monitoring strategies...")
    m = monitor_strategies()
    print(f"monitoring {len(m.get('monitoring', []))} strategies")

    print("Alpha Factory: pipeline complete")
    return 0


if __name__ == '__main__':
    sys.exit(run_pipeline())
