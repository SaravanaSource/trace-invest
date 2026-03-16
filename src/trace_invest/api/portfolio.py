from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from pathlib import Path
import json
from .auth import get_current_user
from datetime import datetime

router = APIRouter(prefix="/portfolio", tags=["portfolio"])

DATA_DIR = Path(__file__).resolve().parents[3] / "data"
PORT_DIR = DATA_DIR / "user_portfolios"
PORT_DIR.mkdir(parents=True, exist_ok=True)


class AddPosition(BaseModel):
    symbol: str
    quantity: float
    price: float


def _user_file(username: str) -> Path:
    return PORT_DIR / f"{username}.json"


@router.get("")
def get_portfolio(user: str = Depends(get_current_user)):
    f = _user_file(user)
    if not f.exists():
        return {"positions": [], "username": user}
    return json.loads(f.read_text())


@router.post("/add")
def add_position(pos: AddPosition, user: str = Depends(get_current_user)):
    f = _user_file(user)
    data = {"positions": [], "username": user, "updated_at": datetime.utcnow().isoformat()+"Z"}
    if f.exists():
        try:
            data = json.loads(f.read_text())
        except Exception:
            pass
    data.setdefault("positions", []).append({"symbol": pos.symbol, "quantity": pos.quantity, "price": pos.price, "added_at": datetime.utcnow().isoformat()+"Z"})
    f.write_text(json.dumps(data, indent=2))
    return data


@router.get("/performance")
def portfolio_performance(user: str = Depends(get_current_user)):
    f = _user_file(user)
    if not f.exists():
        raise HTTPException(status_code=404, detail="no portfolio")
    data = json.loads(f.read_text())
    # simple total return based on last price from history if available
    total = 0.0
    for p in data.get("positions", []):
        total += p.get("quantity", 0) * p.get("price", 0)
    return {"nav": total}
