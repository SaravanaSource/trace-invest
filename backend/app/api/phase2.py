from fastapi import APIRouter, HTTPException
from app.services.phase2 import list_opportunities, build_portfolio_from_snapshot, generate_current_alerts

router = APIRouter(prefix="/phase2", tags=["phase2"])


@router.get("/opportunities")
def get_opportunities():
    try:
        return list_opportunities()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/portfolio")
def get_portfolio():
    try:
        return build_portfolio_from_snapshot()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/alerts")
def get_alerts():
    try:
        return generate_current_alerts()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
