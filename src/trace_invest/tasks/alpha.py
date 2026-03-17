from trace_invest.tasks.celery_app import celery_app
from trace_invest.alpha_factory.signal_lab.signals import discover_signals
from trace_invest.alpha_factory.strategy_generator.generator import generate_strategies
from trace_invest.research.backtesting_engine.backtest import run_backtest
from trace_invest.alpha_factory.strategy_ranking.ranker import rank_strategies
from trace_invest.alpha_factory.strategy_monitor.monitor import monitor_strategies
from trace_invest.db import SessionLocal
from trace_invest.db.models import StrategyResult


@celery_app.task(name="trace_invest.tasks.alpha.run_alpha_pipeline")
def run_alpha_pipeline():
    s = discover_signals()
    g = generate_strategies()
    for strat in g.get("strategies", []):
        name = strat.get("strategy_name")
        positions = strat.get("positions", [])
        res = run_backtest(name, positions)
        # persist to DB for analysis
        try:
            db = SessionLocal()
            sr = StrategyResult(strategy=name, result=res)
            db.add(sr)
            db.commit()
            db.refresh(sr)
            db.close()
        except Exception as _err:
            print(f"Warning: failed to persist strategy result for {name}: {_err}")
    r = rank_strategies()
    m = monitor_strategies()
    return {"signals": len(s.get("signals", [])), "strategies": len(g.get("strategies", [])), "ranked": len(r.get("rankings", []))}
