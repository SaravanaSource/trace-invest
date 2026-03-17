from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from trace_invest.db import SessionLocal
from trace_invest.db.models import Watchlist, User
from trace_invest.api.auth import get_current_user

router = APIRouter(prefix="/watchlist", tags=["watchlist"])


class WatchlistPayload(BaseModel):
    name: str
    symbols: list


@router.post("/create")
def create_watchlist(p: WatchlistPayload, user=Depends(get_current_user)):
    db = SessionLocal()
    username = getattr(user, "username", str(user))
    u = db.query(User).filter(User.username == username).first()
    if not u:
        db.close()
        raise HTTPException(status_code=404, detail="user not found")
    w = Watchlist(user_id=u.id, name=p.name, symbols=p.symbols)
    db.add(w)
    db.commit()
    db.refresh(w)
    db.close()
    return {"id": w.id, "name": w.name, "symbols": w.symbols}


@router.get("/list")
def list_watchlists(user=Depends(get_current_user)):
    db = SessionLocal()
    username = getattr(user, "username", str(user))
    u = db.query(User).filter(User.username == username).first()
    if not u:
        db.close()
        raise HTTPException(status_code=404, detail="user not found")
    rows = db.query(Watchlist).filter(Watchlist.user_id == u.id).all()
    out = [{"id": r.id, "name": r.name, "symbols": r.symbols} for r in rows]
    db.close()
    return {"watchlists": out}


@router.delete("/{name}")
def delete_watchlist(name: str, user=Depends(get_current_user)):
    db = SessionLocal()
    username = getattr(user, "username", str(user))
    u = db.query(User).filter(User.username == username).first()
    if not u:
        db.close()
        raise HTTPException(status_code=404, detail="user not found")
    w = db.query(Watchlist).filter(Watchlist.user_id == u.id, Watchlist.name == name).first()
    if not w:
        db.close()
        raise HTTPException(status_code=404, detail="not found")
    db.delete(w)
    db.commit()
    db.close()
    return {"status": "deleted"}
