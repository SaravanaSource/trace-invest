import json
from pathlib import Path
from typing import Dict, List

from trace_invest.signal_engine.signals import compute_signals, rank_opportunities
from trace_invest.alerts_engine.engine import generate_alerts
from trace_invest.portfolio_engine.engine import build_portfolio
from trace_invest.data_ingestion.financials_fetcher import fetch_financials_from_local

BASE_DIR = Path(__file__).resolve().parents[3]
SNAPSHOT_ROOT = BASE_DIR / "data" / "snapshots"


def _load_latest_snapshot() -> Dict:
    dates = sorted([d.name for d in SNAPSHOT_ROOT.iterdir() if d.is_dir()])
    if not dates:
        return {}
    path = SNAPSHOT_ROOT / dates[-1] / "snapshot.json"
    return json.loads(path.read_text(encoding="utf-8"))


def compute_universe_signals() -> Dict[str, List[Dict]]:
    snap = _load_latest_snapshot()
    decisions = snap.get("decisions", [])
    signals_map: Dict[str, List[Dict]] = {}
    for d in decisions:
        sym = (d.get("symbol") or d.get("stock") or "").upper()
        fin = fetch_financials_from_local(sym) or {}
        # normalize financials payloads: some sources return lists (rows) while
        # signal engine expects a dict of named metrics (e.g., revenue_ttm, fcf_ttm).
        raw_fin = fin.get("financials", {})
        if isinstance(raw_fin, list) and raw_fin:
            # Heuristic: convert first/last dict row into flattened mapping.
            first = raw_fin[0] if isinstance(raw_fin[0], dict) else {}
            flat = {}
            for k, v in first.items():
                try:
                    # try numeric conversion when possible
                    flat[k] = float(v) if (v is not None and (isinstance(v, (int, float)) or str(v).replace('.', '', 1).replace('-', '', 1).isdigit())) else v
                except Exception:
                    flat[k] = v
            processed = {"financials": flat}
        else:
            processed = {"financials": raw_fin or {}}
        history_path = BASE_DIR / "data" / "history" / f"{sym}.json"
        history = {}
        try:
            if history_path.exists():
                history = json.loads(history_path.read_text(encoding="utf-8"))
        except Exception:
            history = {}

        sigs = compute_signals(processed, history)
        signals_map[sym] = sigs

    return signals_map


def list_opportunities() -> List[Dict]:
    signals_map = compute_universe_signals()
    ranked = rank_opportunities(signals_map)
    return ranked


def build_portfolio_from_snapshot() -> Dict:
    snap = _load_latest_snapshot()
    decisions = snap.get("decisions", [])
    signals_map = compute_universe_signals()
    pf = build_portfolio(decisions, signals_map)
    return pf


def generate_current_alerts() -> List[Dict]:
    snap = _load_latest_snapshot()
    decisions = snap.get("decisions", [])
    # load previous snapshot map
    dates = sorted([d.name for d in SNAPSHOT_ROOT.iterdir() if d.is_dir()])
    prev_map = {}
    if len(dates) >= 2:
        prev_path = SNAPSHOT_ROOT / dates[-2] / "snapshot.json"
        try:
            prev_snap = json.loads(prev_path.read_text(encoding="utf-8"))
            for d in prev_snap.get("decisions", []):
                sym = (d.get("symbol") or d.get("stock") or "").upper()
                prev_map[sym] = d
        except Exception:
            prev_map = {}

    signals_map = compute_universe_signals()
    alerts = generate_alerts(decisions, prev_map, signals_map)
    return alerts
