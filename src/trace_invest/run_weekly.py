from pathlib import Path
import json
from datetime import datetime, timezone

from trace_invest.utils.logger import setup_logger
from trace_invest.ingestion.prices import run_weekly_price_ingestion
from trace_invest.validation.runner import run_validation
from trace_invest.intelligence.conviction import conviction_score
from trace_invest.outputs.signals import generate_signal
from trace_invest.outputs.journal import create_journal_entry
from trace_invest.config.loader import load_config
from trace_invest.ingestion.fundamentals import (
    fetch_fundamentals,
    write_raw_fundamentals,
)
from trace_invest.processing.fundamentals import build_processed_fundamentals
from trace_invest.quality.coverage import coverage_score
from trace_invest.quality.freshness import freshness_score
from trace_invest.quality.confidence import confidence_band
from trace_invest.quality.raw_profiler import profile_raw_fundamentals
from trace_invest.quality.raw_schema import inspect_raw_schema
from trace_invest.quality.raw_field_inventory import build_raw_field_inventory


# -----------------------------------------------------------
# Setup
# -----------------------------------------------------------

logger = setup_logger()

SNAPSHOT_DIR = Path("data/snapshots")
SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)


# -----------------------------------------------------------
# Helpers
# -----------------------------------------------------------

def write_processed_fundamentals(snapshot_dir: Path, symbol: str, processed: dict):
    path = snapshot_dir / "fundamentals.json"
    data = json.loads(path.read_text()) if path.exists() else {}
    data[symbol] = processed
    path.write_text(json.dumps(data, indent=2))


def build_validation_financials(processed: dict) -> dict:
    summary = {}

    cashflow = processed.get("cashflow") or []
    if cashflow:
        latest = cashflow[0]
        summary["cash_flow_from_ops"] = next(
            (
                v
                for k, v in latest.items()
                if "Operating Cash Flow" in k
                or "Total Cash From Operating Activities" in k
            ),
            0,
        )

    financials = processed.get("financials") or []
    if financials:
        latest = financials[0]
        summary["net_profit"] = next(
            (
                v
                for k, v in latest.items()
                if "Net Income" in k
                or "Net Profit" in k
            ),
            0,
        )

    return summary


def generate_market_summary(decisions: list) -> dict:
    summary = {
        "total_stocks": len(decisions),
        "by_decision_zone": {},
        "by_overall_risk": {},
    }

    for d in decisions:
        zone = d.get("decision_zone")
        risk = d.get("overall_risk")

        summary["by_decision_zone"][zone] = (
            summary["by_decision_zone"].get(zone, 0) + 1
        )

        summary["by_overall_risk"][risk] = (
            summary["by_overall_risk"].get(risk, 0) + 1
        )

    return summary


# -----------------------------------------------------------
# Main Pipeline
# -----------------------------------------------------------

def run_weekly_pipeline():
    logger.info("===== Weekly TRACE MARKETS run started =====")

    # -------------------------------------------------------
    # Snapshot setup
    # -------------------------------------------------------

    run_date = datetime.now(timezone.utc).date().isoformat()
    snapshot_dir = SNAPSHOT_DIR / run_date
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    snapshot_file = snapshot_dir / "snapshot.json"
    market_summary_file = snapshot_dir / "market_summary.json"

    snapshot = {
        "run_date": run_date,
        "run_timestamp": datetime.now(timezone.utc).isoformat(),
        "decisions": [],
    }

    # -------------------------------------------------------
    # Load config + universe
    # -------------------------------------------------------

    config = load_config()
    # stocks = config["universe"]["universe"]["stocks"]
    stocks = json.loads(Path(config["universe"]["universe"]["stocks_file"]).read_text())
    

    # -------------------------------------------------------
    # Weekly price ingestion
    # -------------------------------------------------------

    run_weekly_price_ingestion()

    # -------------------------------------------------------
    # Per-stock processing
    # -------------------------------------------------------

    for stock in stocks:
        name = stock["name"]
        symbol = stock["symbol"]

        try:
            logger.info(f"Processing {symbol}")

            # Raw fundamentals
            raw_fundamentals = fetch_fundamentals(symbol)
            write_raw_fundamentals(symbol, raw_fundamentals)

            # Processed fundamentals
            processed = build_processed_fundamentals(raw_fundamentals)

            processed["raw_profile"] = profile_raw_fundamentals(raw_fundamentals)
            processed["raw_schema"] = inspect_raw_schema(raw_fundamentals)
            processed["raw_field_inventory"] = build_raw_field_inventory(
                raw_fundamentals
            )

            # Quality layer
            coverage = coverage_score(processed)
            freshness = freshness_score(coverage.get("years", []))
            confidence = confidence_band(coverage, freshness)

            processed["quality"] = {
                "coverage": coverage,
                "freshness": freshness,
                "confidence": confidence,
            }

            write_processed_fundamentals(snapshot_dir, symbol, processed)

            # Validation
            validation = run_validation(processed)

            # Intelligence
            conviction = conviction_score(processed, validation)
            signal = generate_signal(conviction)

            journal = create_journal_entry(name, signal)
            journal["validation"] = validation

            snapshot["decisions"].append(journal)

        except Exception:
            logger.exception(f"FAILED processing {symbol}")
            continue

    # -------------------------------------------------------
    # Market Summary
    # -------------------------------------------------------

    market_summary = generate_market_summary(snapshot["decisions"])
    market_summary_file.write_text(json.dumps(market_summary, indent=2))

    # -------------------------------------------------------
    # Write snapshot
    # -------------------------------------------------------

    snapshot_file.write_text(json.dumps(snapshot, indent=2))

    logger.info(f"Weekly snapshot written: {snapshot_file}")
    logger.info(f"Market summary written: {market_summary_file}")
    logger.info("===== Weekly TRACE MARKETS run completed =====")


# -----------------------------------------------------------
# Entrypoint
# -----------------------------------------------------------

if __name__ == "__main__":
    run_weekly_pipeline()
