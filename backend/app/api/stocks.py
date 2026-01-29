from fastapi import APIRouter, HTTPException
from backend.app.services.snapshot_loader import load_latest_snapshot

router = APIRouter(prefix="/stocks", tags=["stocks"])


@router.get("")
def get_stocks():
    try:
        snapshot = load_latest_snapshot()
        return snapshot["decisions"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{symbol}")
def get_stock(symbol: str):
    try:
        snapshot = load_latest_snapshot()
        decisions = snapshot["decisions"]
        symbol = symbol.upper()

        for stock_obj in decisions:
            if stock_obj.get("stock", "").upper() == symbol:
                return stock_obj

        raise HTTPException(status_code=404, detail="Stock not found")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
