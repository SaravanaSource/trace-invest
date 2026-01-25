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



logger = setup_logger()

SNAPSHOT_DIR = Path("data/snapshots")
SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)


def write_processed_fundamentals(snapshot_dir: Path, symbol: str, processed: dict):
    path = snapshot_dir / "fundamentals.json"
    data = json.loads(path.read_text()) if path.exists() else {}
    data[symbol] = processed
    path.write_text(json.dumps(data, indent=2))


def run_weekly_pipeline():
    logger.info("===== Weekly TRACE MARKETS run started =====")

    # ------------------------------------------------------------------
    # 1. Snapshot setup (MUST be first)
    # ------------------------------------------------------------------
    run_date = datetime.now(timezone.utc).date().isoformat()

    snapshot_dir = SNAPSHOT_DIR / run_date
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    snapshot_file = snapshot_dir / "snapshot.json"

    snapshot = {
        "run_date": run_date,
        "run_timestamp": datetime.now(timezone.utc).isoformat(),
        "decisions": [],
    }

    # ------------------------------------------------------------------
    # 2. Load config + universe
    # ------------------------------------------------------------------
    config = load_config()
    stocks = config["universe"]["universe"]["stocks"]

    # ------------------------------------------------------------------
    # 3. Ingest prices (safe to re-run)
    # ------------------------------------------------------------------
    run_weekly_price_ingestion()

    # ------------------------------------------------------------------
    # 4. Per-stock processing (loop)
    # ------------------------------------------------------------------
    
    def build_validation_financials(processed: dict) -> dict:
        """ Extract scalar financials needed for fraud checks."""
        summary = {}

        # Example extraction from cashflow statement
        cashflow = processed.get("cashflow", [])
        if cashflow:
            latest = cashflow[0]  # most recent row
            summary["cash_flow_from_ops"] = next(
                (v for k, v in latest.items() if "Operating Cash Flow" in k or "Total Cash From Operating Activities" in k),
                0,
            )

        # Example extraction from income statement
        financials = processed.get("financials", [])
        if financials:
            latest = financials[0]
            summary["net_profit"] = next(
                (v for k, v in latest.items() if "Net Income" in k or "Net Profit" in k),
                0,
            )

        return summary

    
    for stock in stocks:
        name = stock["name"]
        symbol = stock["symbol"]

        # Raw fundamentals (immutable)
        raw_fundamentals = fetch_fundamentals(symbol)
        write_raw_fundamentals(symbol, raw_fundamentals)

        # Processed fundamentals (cached)
        processed = build_processed_fundamentals(raw_fundamentals)


        # DEBUG: inspect processed structure ONCE
        if symbol == stocks[0]["symbol"]:
            import pprint
            pprint.pprint(
                {
                    "keys": list(processed.keys()),
                    "income_statement_sample": processed.get("income_statement", [])[:1],
                    "balance_sheet_sample": processed.get("balance_sheet", [])[:1],
                    "cashflow_sample": processed.get("cashflow", [])[:1],
                }
            )


        # Data quality metrics

        coverage = coverage_score(raw_fundamentals)
        freshness = freshness_score(coverage.get("years", []))
        confidence = confidence_band(coverage, freshness)

        processed["quality"] = {
            "coverage": coverage,
            "freshness": freshness,
            "confidence": confidence,
        }

        write_processed_fundamentals(snapshot_dir, symbol, processed)

        # Validation
        validation_financials = build_validation_financials(processed)

        validation = run_validation(
            {
                "financials": validation_financials,
                "governance": processed.get("governance", {}),
            }
        )


        # Intelligence + outputs
        conviction = conviction_score(processed, validation)
        signal = generate_signal(conviction)
        journal = create_journal_entry(name, signal)

        snapshot["decisions"].append(journal)

    # ------------------------------------------------------------------
    # 5. Write snapshot (immutable, once)
    # ------------------------------------------------------------------
    snapshot_file.write_text(json.dumps(snapshot, indent=2))

    logger.info(f"Weekly snapshot written: {snapshot_file}")
    logger.info("===== Weekly TRACE MARKETS run completed =====")


if __name__ == "__main__":
    run_weekly_pipeline()
