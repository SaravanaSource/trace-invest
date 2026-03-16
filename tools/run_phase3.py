"""Phase-3 orchestration pipeline.

Steps performed deterministically:
- load latest snapshot to build universe
- compute factor values for each symbol and write to `data/factors/<SYMBOL>.json`
- load strategy definitions from `data/strategy_definitions/*.json` and run them (writes to `data/strategies`)
- run backtests for generated strategies and write to `data/backtests`
- analyze backtests and write reports to `data/performance_reports`

This script is intentionally read-only for existing artifacts and deterministic.
"""

from pathlib import Path
import json
from typing import Dict, Any

ROOT = Path(__file__).resolve().parents[1]


def _load_latest_snapshot() -> Dict[str, Any]:
    snap_dir = ROOT / "data" / "snapshots"
    if not snap_dir.exists():
        return {}
    dates = sorted([d.name for d in snap_dir.iterdir() if d.is_dir()])
    if not dates:
        return {}
    p = snap_dir / dates[-1] / "snapshot.json"
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def compute_factors_for_universe(universe: Dict[str, Any]):
    from trace_invest.research.factor_library import FACTOR_REGISTRY

    out_dir = ROOT / "data" / "factors"
    out_dir.mkdir(parents=True, exist_ok=True)

    for item in universe:
        sym = item.get("symbol")
        processed = item.get("processed") or {}
        history = item.get("history") or {}
        facts = {}
        for name, fn in FACTOR_REGISTRY.items():
            try:
                res = fn(sym, processed, history)
                facts[name] = res
            except Exception:
                facts[name] = {"symbol": sym, "factor_name": name, "value": None, "metrics_used": [], "explanation": "error"}

        p = out_dir / f"{sym}.json"
        p.write_text(json.dumps(facts, indent=2), encoding="utf-8")


def run_defined_strategies():
    defs_dir = ROOT / "data" / "strategy_definitions"
    outs = []
    if not defs_dir.exists():
        return outs
    from trace_invest.research.strategy_engine.strategy_runner import run_strategy
    for f in defs_dir.glob("*.json"):
        sdef = json.loads(f.read_text(encoding="utf-8"))
        out = run_strategy(sdef)
        outs.append(out)
    return outs


def run_backtests_and_reports():
    from trace_invest.research.backtesting_engine.backtest import run_backtest
    from trace_invest.research.performance_engine.performance import analyze_backtest

    strategies = ROOT / "data" / "strategies"
    if not strategies.exists():
        return
    for s in strategies.iterdir():
        if not s.is_dir():
            continue
        name = s.name
        res_path = s / "results.json"
        if not res_path.exists():
            continue
        res = json.loads(res_path.read_text(encoding="utf-8"))
        positions = res.get("rows", [])
        if positions and "weight" not in positions[0]:
            total = sum([float(r.get("score") or 0) for r in positions]) or 1.0
            for r in positions:
                r["weight"] = float(r.get("score") or 0) / total

        bt = run_backtest(name, positions)
        analyze_backtest(bt)


def main():
    print("Phase-3 pipeline: starting")
    snap = _load_latest_snapshot()
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

    if universe:
        compute_factors_for_universe(universe)
    else:
        print("No universe loaded from snapshots; skipping factor computation")

    run_defined_strategies()
    run_backtests_and_reports()

    print("Phase-3 pipeline: complete")


if __name__ == '__main__':
    main()
