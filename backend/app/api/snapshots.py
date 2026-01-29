from fastapi import APIRouter, HTTPException
from backend.app.services.snapshot_loader import (
    list_snapshot_dates,
    load_snapshot_by_date,
    load_market_summary_by_date
)

router = APIRouter(prefix="/snapshots", tags=["snapshots"])


@router.get("")
def get_snapshot_dates():
    return list_snapshot_dates()


@router.get("/{date}/stocks")
def get_snapshot_stocks(date: str):
    try:
        snapshot = load_snapshot_by_date(date)
        return snapshot["decisions"]
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{date}/market")
def get_snapshot_market(date: str):
    try:
        return load_market_summary_by_date(date)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

