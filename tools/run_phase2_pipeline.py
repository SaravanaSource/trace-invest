"""Orchestrate Phase-2 pipeline end-to-end.

Steps:
 - build snapshot (calls tools/build_snapshot.py)
 - build history for universe
 - compute signals and persist top opportunities
 - build portfolio and persist
 - generate alerts and persist

This script is intentionally deterministic and reads/writes local snapshot artifacts.
"""
from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT_ROOT = ROOT / "data" / "snapshots"
HISTORY_DIR = ROOT / "data" / "history"
SIGNALS_DIR = ROOT / "data" / "signals"
PORTFOLIO_DIR = ROOT / "data" / "portfolio"
ALERTS_DIR = ROOT / "data" / "alerts"

SIGNALS_DIR.mkdir(parents=True, exist_ok=True)
PORTFOLIO_DIR.mkdir(parents=True, exist_ok=True)
ALERTS_DIR.mkdir(parents=True, exist_ok=True)

def run_snapshot():
    print("Running snapshot builder...")
    cmd = [sys.executable, "tools/build_snapshot.py"]
    subprocess.check_call(cmd, cwd=ROOT)


def build_history_all():
    from trace_invest.config.loader import load_config
    from trace_invest.company_history_engine import build_company_history

    cfg = load_config()
    stocks = cfg.get("universe", {}).get("universe", {}).get("stocks", [])
    for s in stocks:
        sym = s.get("symbol")
        if sym:
            print(f"Building history for {sym}")
            build_company_history(sym)


def compute_and_persist():
    from backend.app.services.phase2 import compute_universe_signals, list_opportunities, build_portfolio_from_snapshot, generate_current_alerts

    print("Computing universe signals...")
    signals_map = compute_universe_signals()

    print("Building and persisting opportunities...")
    opportunities = list_opportunities()
    (SIGNALS_DIR / "top_opportunities.json").write_text(json.dumps(opportunities, indent=2), encoding="utf-8")

    print("Building portfolio...")
    portfolio = build_portfolio_from_snapshot()
    (PORTFOLIO_DIR / "portfolio.json").write_text(json.dumps(portfolio, indent=2), encoding="utf-8")

    print("Generating alerts...")
    alerts = generate_current_alerts()
    (ALERTS_DIR / "alerts.json").write_text(json.dumps(alerts, indent=2), encoding="utf-8")


def main():
    run_snapshot()
    build_history_all()
    compute_and_persist()
    print("Phase-2 pipeline complete. Artifacts in data/history, data/signals, data/portfolio, data/alerts")


if __name__ == "__main__":
    main()
