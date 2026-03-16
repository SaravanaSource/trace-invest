"""Verify Phase-3 integrity and produce a verification report."""
from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]


def main():
    report = {"time": datetime.utcnow().isoformat() + "Z", "checks": []}

    try:
        from tools.run_phase3 import _load_latest_snapshot, compute_factors_for_universe, run_defined_strategies, run_backtests_and_reports
    except Exception:
        report["checks"].append({"name": "import_run_phase3", "ok": False, "note": "cannot import run_phase3 functions"})
        _write_report(report)
        return

    snap = _load_latest_snapshot()
    if not snap:
        report["checks"].append({"name": "snapshot_present", "ok": False, "note": "no snapshot found"})
        _write_report(report)
        return
    else:
        report["checks"].append({"name": "snapshot_present", "ok": True, "note": f"decisions={len(snap.get('decisions',[]))}"})

    # build minimal universe
    decisions = snap.get("decisions", [])
    universe = []
    from trace_invest.data_ingestion.financials_fetcher import fetch_financials_from_local
    for d in decisions[:20]:
        sym = (d.get("symbol") or d.get("stock") or "").upper()
        fin = fetch_financials_from_local(sym) or {}
        processed = {"financials": fin.get("financials", {})}
        hist = {}
        p = ROOT / "data" / "history" / f"{sym}.json"
        if p.exists():
            hist = json.loads(p.read_text(encoding="utf-8"))
        universe.append({"symbol": sym, "processed": processed, "history": hist})

    try:
        compute_factors_for_universe(universe)
        factors_dir = ROOT / "data" / "factors"
        ok = factors_dir.exists() and any(factors_dir.glob("*.json"))
        report["checks"].append({"name": "factors_generated", "ok": bool(ok)})
    except Exception as e:
        report["checks"].append({"name": "factors_generated", "ok": False, "note": str(e)})

    try:
        outs = run_defined_strategies()
        strategies_dir = ROOT / "data" / "strategies"
        ok = strategies_dir.exists()
        report["checks"].append({"name": "strategies_run", "ok": bool(ok), "note": f"outputs={len(list(strategies_dir.iterdir())) if ok else 0}"})
    except Exception as e:
        report["checks"].append({"name": "strategies_run", "ok": False, "note": str(e)})

    try:
        run_backtests_and_reports()
        backtests_dir = ROOT / "data" / "backtests"
        perf_dir = ROOT / "data" / "performance_reports"
        report["checks"].append({"name": "backtests_present", "ok": bool(backtests_dir.exists() and any(backtests_dir.glob("*.json")))})
        report["checks"].append({"name": "performance_reports_present", "ok": bool(perf_dir.exists() and any(perf_dir.glob("*.json")))})
    except Exception as e:
        report["checks"].append({"name": "backtests_and_reports", "ok": False, "note": str(e)})

    _write_report(report)


def _write_report(report: dict):
    out = ROOT / "PHASE3_VERIFICATION_REPORT.md"
    lines = ["# PHASE3 VERIFICATION REPORT", "", f"Generated: {report.get('time')}", ""]
    for c in report.get("checks", []):
        lines.append(f"- **{c.get('name')}**: {'OK' if c.get('ok') else 'FAIL'}{(' - ' + c.get('note')) if c.get('note') else ''}")
    out.write_text("\n".join(lines), encoding="utf-8")
    print("Wrote:", out)


if __name__ == '__main__':
    main()
