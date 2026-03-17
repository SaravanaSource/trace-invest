"""Orchestration script for Phase-4 Alpha Factory pipeline."""
from pathlib import Path
from trace_invest.alpha_factory.signal_lab.signals import discover_signals
from trace_invest.alpha_factory.strategy_generator.generator import generate_strategies
from trace_invest.alpha_factory.strategy_ranking.ranker import rank_strategies
from trace_invest.alpha_factory.strategy_monitor.monitor import monitor_strategies
import json
import sys
from trace_invest.config import data_path, ensure_data_dirs
from trace_invest.research.backtesting_engine.backtest import run_backtest
from trace_invest.db import SessionLocal
from trace_invest.db.models import StrategyResult


def run_pipeline():
    ensure_data_dirs("backtests", "insights")
    data_dir = data_path()
    print("Alpha Factory: running signal discovery...")
    s = discover_signals()
    print(f"discovered {len(s.get('signals', []))} signals")

    print("Alpha Factory: generating strategies...")
    g = generate_strategies()
    print(f"generated {len(g.get('strategies', []))} strategies")

    # backtests: run the real backtester for each generated strategy
    bt_dir = data_path("backtests")
    bt_dir.mkdir(parents=True, exist_ok=True)
    for strat in g.get("strategies", []):
        name = strat.get("strategy_name")
        positions = strat.get("positions", [])
        try:
            print(f"Running backtest for {name}...")
            res = run_backtest(name, positions)
            print(f"backtest {name}: CAGR={res.get('CAGR')}, sharpe={res.get('sharpe_ratio')}")
            # persist result to DB for later analysis
            try:
                db = SessionLocal()
                sr = StrategyResult(strategy=name, result=res)
                db.add(sr)
                db.commit()
                db.refresh(sr)
                db.close()
            except Exception as _err:
                print(f"Warning: failed to persist strategy result for {name}: {_err}")
        except Exception as exc:
            print(f"Backtest failed for {name}: {exc}")

    print("Alpha Factory: ranking strategies...")
    r = rank_strategies()
    print(f"ranked {len(r.get('rankings', []))} strategies")

    # persist simple insights to data/insights for quick inspection
    try:
        insights_dir = data_path("insights")
        insights_dir.mkdir(parents=True, exist_ok=True)
        (insights_dir / "rankings.json").write_text(json.dumps(r, indent=2))
    except Exception as _err:
        print(f"Warning: failed to write insights: {_err}")

    print("Alpha Factory: monitoring strategies...")
    m = monitor_strategies()
    print(f"monitoring {len(m.get('monitoring', []))} strategies")

    print("Alpha Factory: pipeline complete")
    return 0


if __name__ == '__main__':
    sys.exit(run_pipeline())
