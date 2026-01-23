from pathlib import Path
from datetime import datetime
import yfinance as yf
import json

from trace_invest.utils.logger import setup_logger

logger = setup_logger()

RAW_DIR = Path("data/raw/fundamentals")
RAW_DIR.mkdir(parents=True, exist_ok=True)

def _df_to_serializable(df):
    """
    Convert pandas DataFrame to JSON-serializable structure.
    """
    if df is None or df.empty:
        return []

    df = df.copy()
    df.columns = [str(c) for c in df.columns]
    df.index = df.index.astype(str)

    return df.reset_index().to_dict(orient="records")


def fetch_fundamentals(symbol: str) -> dict:
    logger.info(f"Fetching fundamentals for {symbol}")
    ticker = yf.Ticker(symbol)

    data = {
        "symbol": symbol,
        "fetched_at": datetime.utcnow().isoformat(),
        "financials": _df_to_serializable(ticker.financials),
        "balance_sheet": _df_to_serializable(ticker.balance_sheet),
        "cashflow": _df_to_serializable(ticker.cashflow),
        "info": ticker.info or {},
    }
    return data



def write_raw_fundamentals(symbol: str, data: dict) -> Path:
    path = RAW_DIR / f"{symbol.replace('.', '_')}.json"
    if path.exists():
        logger.info(f"Raw fundamentals already exist for {symbol}, skipping")
        return path

    path.write_text(json.dumps(data, indent=2))
    logger.info(f"Raw fundamentals written for {symbol}")
    return path

