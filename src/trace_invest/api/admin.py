from fastapi import APIRouter
from trace_invest.db import SessionLocal
from trace_invest.db.models import StrategyResult

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/metrics")
def metrics():
    db = SessionLocal()
    try:
        sr_count = db.query(StrategyResult).count()
    except Exception as e:
        db.close()
        return {"error": str(e)}
    db.close()
    # queue length inspection via redis if available
    try:
        import os
        import redis
        broker = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
        r = redis.from_url(broker)
        # common list names: 'celery' or 'celery' prefixed keys
        qlen = 0
        try:
            qlen = r.llen('celery')
        except Exception:
            try:
                qlen = r.llen('queue:alpha')
            except Exception:
                qlen = 0
        return {"strategy_results": sr_count, "queue_length": qlen}
    except Exception as e:
        return {"strategy_results": sr_count, "queue_length": None, "broker_error": str(e)}
