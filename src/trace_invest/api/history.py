from fastapi import APIRouter
from trace_invest.memory.reader import load_stock_history

router = APIRouter(prefix="/history", tags=["history"])


@router.get("/{symbol}")
def get_history(symbol: str):
    symbol = symbol.upper()
    history = load_stock_history(symbol)
    history.sort(key=lambda r: r.get("date") or "", reverse=True)
    print("HISTORY LOADED", symbol, len(history))
    return {
        "symbol": symbol,
        "history": history,
    }
