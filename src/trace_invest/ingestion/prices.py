from datetime import datetime
import json
from pathlib import Path
import pandas as pd
import yfinance as yf

from trace_invest.config.loader import load_config
from trace_invest.utils.logger import setup_logger

logger = setup_logger()

RAW_DATA_DIR = Path("data/raw/prices")
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)


class PriceIngestionError(Exception):
    pass


def fetch_weekly_prices(symbol: str) -> pd.DataFrame:
    """
    Fetch weekly OHLCV data using Yahoo Finance.
    """
    logger.info(f"Fetching weekly prices for {symbol}")

    ticker = yf.Ticker(symbol)
    df = ticker.history(period="max", interval="1wk", auto_adjust=False)

    if df.empty:
        raise PriceIngestionError(f"No price data returned for {symbol}")

    df.reset_index(inplace=True)
    df["symbol"] = symbol
    df["source"] = "yahoo_finance"
    df["ingested_at"] = datetime.utcnow().isoformat()

    return df


def write_raw_prices(symbol: str, df: pd.DataFrame) -> None:
    file_path = RAW_DATA_DIR / f"{symbol.replace('.', '_')}.csv"

    if file_path.exists():
        logger.warning(f"Raw price file already exists for {symbol}. Skipping write.")
        return

    df.to_csv(file_path, index=False)
    logger.info(f"Raw weekly prices written for {symbol}")


def run_weekly_price_ingestion() -> None:
    config = load_config()
    # stocks = config["universe"]["universe"]["stocks"]
    stocks = json.loads(Path(config["universe"]["universe"]["stocks_file"]).read_text())

    logger.info("Starting weekly price ingestion")

    for stock in stocks:
        symbol = stock["symbol"]
        try:
            df = fetch_weekly_prices(symbol)
            write_raw_prices(symbol, df)
        except Exception as e:
            logger.error(f"Failed to ingest prices for {symbol}: {e}")

    logger.info("Weekly price ingestion completed")
