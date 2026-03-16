"""Phase-3 orchestration: compute factors, run strategy, backtest, performance reports."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

def main():
    print("Phase-3 orchestration: generating sample factor outputs and running a demo strategy")
    # demo: compute factors for universe by reusing existing snapshot decisions
    snap_dir = ROOT / "data" / "snapshots"
    dates = sorted([d.name for d in snap_dir.iterdir() if d.is_dir()])
    if not dates:
        print("No snapshots found; run snapshot first")
        return
    snap = json.loads((snap_dir / dates[-1] / "snapshot.json").read_text(encoding="utf-8"))
    decisions = snap.get("decisions", [])
    universe = []
    from trace_invest.data_ingestion.financials_fetcher import fetch_financials_from_local
    for d in decisions:
        sym = (d.get("symbol") or d.get("stock") or "").upper()
        fin = fetch_financials_from_local(sym) or {}
        processed = {"financials": fin.get("financials", {})}
        hist = {}
        path = ROOT / "data" / "history" / f"{sym}.json"
        if path.exists():
            hist = json.loads(path.read_text(encoding="utf-8"))
        universe.append({"symbol": sym, "processed": processed, "history": hist})

    # demo strategy
    strategy = {"name": "Quality Growth", "rules": ["ROE > 18"], "ranking": {"top_n": 20}}
    from trace_invest.research.strategy_engine.strategy_runner import run_strategy
    out = run_strategy(strategy, universe)
    print(f"Strategy returned {len(out)} symbols")

    # run simple backtest if prices exist
    from trace_invest.research.backtesting_engine.backtest import run_backtest
    price_series = {}
    for u in universe:
        sym = u["symbol"]
        p = ROOT / "data" / "raw" / "prices" / f"{sym.replace('.','_')}.csv"
        if p.exists():
            # load csv minimal
            import csv
            rows = []
            with p.open() as fh:
                rdr = csv.DictReader(fh)
                for r in rdr:
                    rows.append({"date": r.get("Date"), "close": r.get("Close")})
            price_series[sym] = rows
    if price_series:
        res = run_backtest("quality_growth_demo", price_series, "2015-01-01", "2025-01-01")
        print("Backtest:", res)

    print("Phase-3 demo complete")


if __name__ == '__main__':
    main()
"""Run Phase-3 research pipeline:
 - run Phase-2 pipeline (to ensure snapshots/signals exist)
 - run strategy definitions under data/strategies_definitions (if present)
 - run backtests for generated strategies
 - compute performance reports
"""
from pathlib import Path
import subprocess
import sys
import json

ROOT = Path(__file__).resolve().parents[1]


def run_phase2():
    subprocess.check_call([sys.executable, "tools/run_phase2_pipeline.py"], cwd=ROOT)


def run_strategies():
    defs_dir = ROOT / "data" / "strategy_definitions"
    from trace_invest.research.strategy_engine.strategy_runner import run_strategy
    if not defs_dir.exists():
        return []
    outs = []
    for f in defs_dir.glob("*.json"):
        sdef = json.loads(f.read_text(encoding="utf-8"))
        out = run_strategy(sdef)
        outs.append(out)
    return outs


def run_backtests():
    from trace_invest.research.backtesting_engine.backtest import run_backtest
    from trace_invest.research.performance_engine.performance import analyze_backtest
    strategies = Path("data/strategies")
    if not strategies.exists():
        return
    for s in strategies.iterdir():
        if not s.is_dir():
            continue
        name = s.name
        res = json.loads((s / "results.json").read_text(encoding="utf-8"))
        positions = res.get("rows", [])
        # map rows to weights if not present
        if positions and "weight" not in positions[0]:
            total = sum([r.get("score") or 0 for r in positions]) or 1
            for r in positions:
                r["weight"] = (r.get("score") or 0) / total

        bt = run_backtest(name, positions)
        analyze_backtest(bt)


def main():
    run_phase2()
    run_strategies()
    run_backtests()
    print("Phase-3 pipeline complete")


if __name__ == '__main__':
    main()
