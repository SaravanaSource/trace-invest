from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime
import json

from trace_invest.api.auth import get_current_user
from trace_invest.db import SessionLocal
from trace_invest.db.models import Portfolio, User
from trace_invest.config import data_path

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


class AddPosition(BaseModel):
    symbol: str
    quantity: float
    price: float


def _read_market_prices():
    p = data_path("market_prices.json")
    try:
        return json.loads(p.read_text())
    except Exception:
        return {}


@router.get("")
def get_portfolio(user=Depends(get_current_user)):
    db = SessionLocal()
    # `user` may be a User object from get_current_user
    username = getattr(user, "username", str(user))
    u = db.query(User).filter(User.username == username).first()
    if not u:
        db.close()
        raise HTTPException(status_code=404, detail="user not found")
    p = db.query(Portfolio).filter(Portfolio.user_id == u.id).all()
    out = {"username": username, "positions": []}
    for port in p:
        out["positions"].extend(port.holdings or [])
    db.close()
    return out


@router.post("/add")
def add_position(pos: AddPosition, user=Depends(get_current_user)):
    db = SessionLocal()
    username = getattr(user, "username", str(user))
    u = db.query(User).filter(User.username == username).first()
    if not u:
        db.close()
        raise HTTPException(status_code=404, detail="user not found")
    # create or append to a default portfolio named 'default'
    portfolio = db.query(Portfolio).filter(Portfolio.user_id == u.id, Portfolio.name == 'default').first()
    if not portfolio:
        portfolio = Portfolio(user_id=u.id, name='default', holdings=[])
    holdings = portfolio.holdings or []
    holdings.append({"symbol": pos.symbol, "quantity": pos.quantity, "price": pos.price, "added_at": datetime.utcnow().isoformat()+"Z"})
    portfolio.holdings = holdings
    db.add(portfolio)
    db.commit()
    db.refresh(portfolio)
    db.close()
    return {"username": username, "positions": portfolio.holdings}


@router.get("/performance")
def portfolio_performance(user=Depends(get_current_user)):
    db = SessionLocal()
    username = getattr(user, "username", str(user))
    u = db.query(User).filter(User.username == username).first()
    if not u:
        db.close()
        raise HTTPException(status_code=404, detail="user not found")
    p = db.query(Portfolio).filter(Portfolio.user_id == u.id).all()
    market = _read_market_prices()
    total = 0.0
    for port in p:
        for h in (port.holdings or []):
            qty = h.get("quantity", 0)
            sym = h.get("symbol")
            price = market.get(sym, {}).get("last_price") or h.get("price") or 0
            total += qty * float(price)
    db.close()
    return {"nav": total}



@router.get("/list")
def list_portfolios(user=Depends(get_current_user)):
    db = SessionLocal()
    username = getattr(user, "username", str(user))
    u = db.query(User).filter(User.username == username).first()
    if not u:
        db.close()
        raise HTTPException(status_code=404, detail="user not found")
    ports = db.query(Portfolio).filter(Portfolio.user_id == u.id).all()
    out = [{"id": p.id, "name": p.name, "holdings_count": len(p.holdings or [])} for p in ports]
    db.close()
    return {"portfolios": out}


@router.get("/{name}")
def get_portfolio_by_name(name: str, user=Depends(get_current_user)):
    db = SessionLocal()
    username = getattr(user, "username", str(user))
    u = db.query(User).filter(User.username == username).first()
    if not u:
        db.close()
        raise HTTPException(status_code=404, detail="user not found")
    port = db.query(Portfolio).filter(Portfolio.user_id == u.id, Portfolio.name == name).first()
    if not port:
        db.close()
        raise HTTPException(status_code=404, detail="portfolio not found")
    out = {"id": port.id, "name": port.name, "holdings": port.holdings}
    db.close()
    return out


@router.put("/{name}")
def upsert_portfolio(name: str, payload: dict, user=Depends(get_current_user)):
    db = SessionLocal()
    username = getattr(user, "username", str(user))
    u = db.query(User).filter(User.username == username).first()
    if not u:
        db.close()
        raise HTTPException(status_code=404, detail="user not found")
    port = db.query(Portfolio).filter(Portfolio.user_id == u.id, Portfolio.name == name).first()
    if not port:
        port = Portfolio(user_id=u.id, name=name, holdings=payload.get("holdings", []))
    else:
        port.holdings = payload.get("holdings", port.holdings or [])
    db.add(port)
    db.commit()
    db.refresh(port)
    db.close()
    return {"id": port.id, "name": port.name, "holdings": port.holdings}


@router.delete("/{name}")
def delete_portfolio(name: str, user=Depends(get_current_user)):
    db = SessionLocal()
    username = getattr(user, "username", str(user))
    u = db.query(User).filter(User.username == username).first()
    if not u:
        db.close()
        raise HTTPException(status_code=404, detail="user not found")
    port = db.query(Portfolio).filter(Portfolio.user_id == u.id, Portfolio.name == name).first()
    if not port:
        db.close()
        raise HTTPException(status_code=404, detail="portfolio not found")
    db.delete(port)
    db.commit()
    db.close()
    return {"status": "deleted"}


@router.get("/analytics/exposure")
def portfolio_exposure(user=Depends(get_current_user)):
    db = SessionLocal()
    username = getattr(user, "username", str(user))
    u = db.query(User).filter(User.username == username).first()
    if not u:
        db.close()
        raise HTTPException(status_code=404, detail="user not found")
    p = db.query(Portfolio).filter(Portfolio.user_id == u.id).all()
    exposure = {}
    for port in p:
        for h in (port.holdings or []):
            sym = h.get("symbol")
            w = float(h.get("quantity", 0))
            exposure[sym] = exposure.get(sym, 0.0) + w
    db.close()
    return {"exposure": exposure}
