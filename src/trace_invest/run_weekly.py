from trace_invest.utils.logger import setup_logger
from trace_invest.ingestion.prices import run_weekly_price_ingestion
from trace_invest.validation.runner import run_validation
from trace_invest.intelligence.conviction import conviction_score
from trace_invest.outputs.signals import generate_signal
from trace_invest.outputs.journal import create_journal_entry
from trace_invest.config.loader import load_config
from trace_invest.ingestion.fundamentals import (fetch_fundamentals,write_raw_fundamentals,)
from trace_invest.processing.fundamentals import build_processed_fundamentals


from pathlib import Path
import json
from datetime import datetime

logger = setup_logger()

SNAPSHOT_DIR = Path("data/snapshots")
SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)


def run_weekly_pipeline():
    logger.info("===== Weekly Trace Invest run started =====")

    config = load_config()
    stocks = config["universe"]["universe"]["stocks"]

    # 1. Ingest prices (safe to re-run)
    run_weekly_price_ingestion()

    snapshot = {
        "run_timestamp": datetime.utcnow().isoformat(),
        "decisions": [],
    }

    for stock in stocks:
        name = stock["name"]
        symbol = stock["symbol"]

        # 1. Fetch + store raw fundamentals (immutable)
        raw_fundamentals = fetch_fundamentals(symbol)
        write_raw_fundamentals(symbol, raw_fundamentals)

        # 2. Build processed fundamentals (explainable metrics)
        processed = build_processed_fundamentals(raw_fundamentals)

        # 3. Run fraud & governance validation
        validation = run_validation(
            {
                "financials": processed.get("financials", {}),
                "governance": processed.get("governance", {}),
            }
        )

        # 4. Intelligence + outputs
        conviction = conviction_score(processed, validation)
        signal = generate_signal(conviction)
        journal = create_journal_entry(name, signal)

        snapshot["decisions"].append(journal)


    # 2. Write snapshot (immutable)
    snapshot_file = SNAPSHOT_DIR / f"weekly_{datetime.utcnow().date()}.json"
    snapshot_file.write_text(json.dumps(snapshot, indent=2))

    logger.info(f"Weekly snapshot written: {snapshot_file}")
    logger.info("===== Weekly Trace Invest run completed =====")


if __name__ == "__main__":
    run_weekly_pipeline()

