from __future__ import annotations

from pathlib import Path
import json
import hashlib
from datetime import datetime, timezone
from typing import Dict, List, Optional

from zoneinfo import ZoneInfo

from trace_invest.config.loader import load_config
from trace_invest.processing.fundamentals import build_processed_fundamentals
from trace_invest.validation.runner import run_validation
from trace_invest.validation.system_awareness import build_system_awareness
from trace_invest.intelligence.conviction import conviction_score
from trace_invest.outputs.signals import generate_signal
from trace_invest.outputs.narrative import generate_narrative
from trace_invest.quality.coverage import coverage_score
from trace_invest.quality.freshness import freshness_score
from trace_invest.quality.confidence import confidence_band
from trace_invest.utils.logger import setup_logger

from trace_invest.pipeline.delta import build_snapshot_deltas
from trace_invest.pipeline.market_summary import generate_market_summary
from trace_invest.pipeline.reasoning_story import (
    build_reasoning_story,
    reasoning_story_filename,
)


SNAPSHOT_SCHEMA_VERSION = "v1"
RAW_DIR = Path("data/raw/fundamentals")
SNAPSHOT_ROOT = Path("data/snapshots")
CONFIG_DIR = Path("configs")


logger = setup_logger()


def build_snapshot(run_date: Optional[str] = None) -> Dict:
    config = load_config()
    run_date = run_date or _today_in_timezone(config)

    snapshot_dir = SNAPSHOT_ROOT / run_date
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    run_timestamp = datetime.now(timezone.utc).isoformat()

    # Build decisions using the single run timestamp to keep snapshots deterministic
    decisions = _build_decisions(config, run_timestamp)
    decisions = sorted(decisions, key=lambda d: (d.get("stock") or "").upper())

    previous_snapshot = _load_previous_snapshot(run_date)
    decisions, delta_stats = build_snapshot_deltas(decisions, previous_snapshot)

    snapshot = {
        "schema_version": SNAPSHOT_SCHEMA_VERSION,
        "run_date": run_date,
        "run_timestamp": run_timestamp,
        "decisions": decisions,
    }

    market_summary = generate_market_summary(decisions, delta_stats)
    metadata = _build_metadata(run_date, run_timestamp, decisions)

    _write_reasoning_stories(snapshot_dir, snapshot, decisions)

    _write_json(snapshot_dir / "snapshot.json", snapshot)
    _write_json(snapshot_dir / "market_summary.json", market_summary)
    _write_json(snapshot_dir / "metadata.json", metadata)

    return {
        "snapshot": snapshot,
        "market_summary": market_summary,
        "metadata": metadata,
    }


def _write_reasoning_stories(snapshot_dir: Path, snapshot: Dict, decisions: List[Dict]) -> None:
    reasoning_dir = snapshot_dir / "reasoning"
    reasoning_dir.mkdir(parents=True, exist_ok=True)

    for decision in decisions:
        story = build_reasoning_story(decision, snapshot)
        filename = reasoning_story_filename(decision)
        _write_json(reasoning_dir / filename, story)


def _build_decisions(config: Dict, run_timestamp: str) -> List[Dict]:
    universe = _load_universe(config)
    decisions: List[Dict] = []

    for stock in universe:
        name = stock.get("name")
        symbol = stock.get("symbol")
        if not symbol:
            logger.warning("Skipping stock with missing symbol: {}", stock)
            continue

        raw = _load_raw_fundamentals(symbol)
        if not raw:
            logger.warning("Missing raw fundamentals for {}", symbol)
            continue

        processed = build_processed_fundamentals(raw)
        coverage = coverage_score(processed)
        freshness = freshness_score(coverage.get("years", []))
        confidence = confidence_band(coverage, freshness)

        validation = run_validation(processed)
        conviction = conviction_score(processed, validation)
        signal = generate_signal(conviction)

        narrative = generate_narrative({"validation": validation})
        valuation_sanity = _extract_valuation_status(validation)

        decision = {
            # Use the snapshot run timestamp so repeated runs with identical inputs
            # produce identical outputs (deterministic and auditable).
            "timestamp": run_timestamp,
            "stock": name or symbol,
            "symbol": symbol,
            "decision_zone": signal.get("zone"),
            "conviction_score": int(round(signal.get("conviction_score", 0))),
            "overall_risk": validation.get("overall_risk"),
            "data_confidence_score": validation.get("data_confidence_score"),
            "data_confidence_band": validation.get("data_confidence_band"),
            "narrative": narrative,
            "master": validation.get("master"),
            "governance": validation.get("governance"),
            "stability": validation.get("stability"),
            "valuation": {
                "valuation_sanity": valuation_sanity,
            },
            "quality": {
                "confidence_band": confidence,
            },
            "trend": {
                "trend": "NO_DATA",
                "delta": None,
            },
            "validation": validation,
        }

        decision["system_awareness"] = build_system_awareness(decision, validation)

        decisions.append(decision)

    return decisions


def _load_universe(config: Dict) -> List[Dict]:
    universe = config.get("universe", {}).get("universe", {})
    stocks = universe.get("stocks") or []

    if stocks:
        return stocks

    stocks_file = universe.get("stocks_file")
    if not stocks_file:
        return []

    path = Path(stocks_file)
    if not path.exists():
        logger.warning("Universe stocks_file not found: {}", path)
        return []

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        logger.warning("Failed to read universe file {}: {}", path, exc)
        return []

    return data if isinstance(data, list) else []


def _load_raw_fundamentals(symbol: str) -> Optional[Dict]:
    filename = f"{symbol.replace('.', '_').upper()}.json"
    path = RAW_DIR / filename

    if not path.exists():
        return None

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        logger.warning("Failed to read raw fundamentals {}: {}", path, exc)
        return None


def _load_previous_snapshot(run_date: str) -> Optional[Dict]:
    if not SNAPSHOT_ROOT.exists():
        return None

    dates = [
        d.name for d in SNAPSHOT_ROOT.iterdir()
        if d.is_dir()
    ]

    previous_dates = sorted(d for d in dates if d < run_date)
    if not previous_dates:
        return None

    previous_dir = SNAPSHOT_ROOT / previous_dates[-1]
    snapshot_file = previous_dir / "snapshot.json"
    if not snapshot_file.exists():
        return None

    try:
        return json.loads(snapshot_file.read_text(encoding="utf-8"))
    except Exception as exc:
        logger.warning("Failed to load previous snapshot {}: {}", snapshot_file, exc)
        return None


def _extract_valuation_status(validation: Dict) -> Optional[str]:
    valuation = validation.get("details", {}).get("valuation_sanity")
    if isinstance(valuation, dict):
        return valuation.get("status")
    return valuation


def _today_in_timezone(config: Dict) -> str:
    tz_name = config.get("system", {}).get("timezone", "UTC")
    try:
        tz = ZoneInfo(tz_name)
    except Exception:
        tz = timezone.utc

    return datetime.now(tz).date().isoformat()


def _write_json(path: Path, payload: Dict) -> None:
    path.write_text(
        json.dumps(_sanitize(payload), indent=2, sort_keys=True),
        encoding="utf-8",
    )


def _sanitize(obj):
    if isinstance(obj, float):
        if obj != obj or obj in (float("inf"), float("-inf")):
            return None
        return obj
    if isinstance(obj, dict):
        return {k: _sanitize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_sanitize(v) for v in obj]
    return obj


def _build_metadata(run_date: str, run_timestamp: str, decisions: List[Dict]) -> Dict:
    config_files = [
        "system.yaml",
        "universe.yaml",
        "risk.yaml",
        "data_sources.yaml",
    ]

    configs = []
    for filename in config_files:
        path = CONFIG_DIR / filename
        if path.exists():
            configs.append({
                "path": str(path).replace("\\", "/"),
                "sha256": _hash_file(path),
            })

    inputs = []
    for decision in decisions:
        symbol = decision.get("symbol")
        if not symbol:
            continue
        filename = f"{symbol.replace('.', '_').upper()}.json"
        path = RAW_DIR / filename
        if path.exists():
            inputs.append({
                "path": str(path).replace("\\", "/"),
                "sha256": _hash_file(path),
            })

    return {
        "schema_version": SNAPSHOT_SCHEMA_VERSION,
        "run_date": run_date,
        "run_timestamp": run_timestamp,
        "config_files": configs,
        "input_files": inputs,
    }


def _hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()
