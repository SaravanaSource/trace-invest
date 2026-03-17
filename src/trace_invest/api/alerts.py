from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from trace_invest.db import SessionLocal
from trace_invest.db.models import Alert, User
from trace_invest.api.auth import get_current_user

router = APIRouter(prefix="/alerts", tags=["alerts"])


class AlertPayload(BaseModel):
    alert_type: str
    payload: dict


@router.post("/create")
def create_alert(p: AlertPayload, user=Depends(get_current_user)):
    db = SessionLocal()
    username = getattr(user, "username", str(user))
    u = db.query(User).filter(User.username == username).first()
    if not u:
        db.close()
        raise HTTPException(status_code=404, detail="user not found")
    a = Alert(user_id=u.id, alert_type=p.alert_type, payload=p.payload)
    db.add(a)
    db.commit()
    db.refresh(a)
    db.close()
    return {"id": a.id, "type": a.alert_type}


@router.get("/list")
def list_alerts(user=Depends(get_current_user)):
    db = SessionLocal()
    username = getattr(user, "username", str(user))
    u = db.query(User).filter(User.username == username).first()
    if not u:
        db.close()
        raise HTTPException(status_code=404, detail="user not found")
    rows = db.query(Alert).filter(Alert.user_id == u.id).order_by(Alert.created_at.desc()).all()
    out = [{"id": r.id, "type": r.alert_type, "payload": r.payload, "is_read": r.is_read} for r in rows]
    db.close()
    return {"alerts": out}


@router.post("/mark_read/{id}")
def mark_read(id: int, user=Depends(get_current_user)):
    db = SessionLocal()
    a = db.query(Alert).filter(Alert.id == id).first()
    if not a:
        db.close()
        raise HTTPException(status_code=404, detail="not found")
    a.is_read = True
    db.add(a)
    db.commit()
    db.close()
    return {"status": "ok"}
