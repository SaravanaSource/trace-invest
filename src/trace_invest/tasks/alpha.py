from trace_invest.tasks.celery_app import celery_app
from trace_invest.alpha_factory.signal_lab.signals import discover_signals
from trace_invest.alpha_factory.strategy_generator.generator import generate_strategies
from trace_invest.research.backtesting_engine.backtest import run_backtest
from trace_invest.alpha_factory.strategy_ranking.ranker import rank_strategies
from trace_invest.alpha_factory.strategy_monitor.monitor import monitor_strategies


@celery_app.task(name="trace_invest.tasks.alpha.run_alpha_pipeline")
def run_alpha_pipeline():
    s = discover_signals()
    g = generate_strategies()
    for strat in g.get("strategies", []):
        name = strat.get("strategy_name")
        positions = strat.get("positions", [])
        run_backtest(name, positions)
    r = rank_strategies()
    m = monitor_strategies()
    return {"signals": len(s.get("signals", [])), "strategies": len(g.get("strategies", [])), "ranked": len(r.get("rankings", []))}
