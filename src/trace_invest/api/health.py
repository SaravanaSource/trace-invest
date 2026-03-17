from fastapi import APIRouter
from trace_invest.db import SessionLocal, engine
import json

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health():
    status = {"db": False, "broker": None}
    try:
        # quick db check
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        status["db"] = True
    except Exception as e:
        status["db_error"] = str(e)

    # broker health: try redis ping if available
    try:
        import redis
        import os

        broker = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
        # parse host/port naive
        r = redis.from_url(broker)
        status["broker"] = "ok" if r.ping() else "unreachable"
    except Exception as e:
        status["broker_error"] = str(e)

    return status
