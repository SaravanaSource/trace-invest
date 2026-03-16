from celery import Celery
import os

BROKER = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")

celery_app = Celery("trace_invest_tasks", broker=BROKER, backend=BACKEND)
celery_app.conf.task_routes = {"trace_invest.tasks.alpha.run_alpha_pipeline": {"queue": "alpha"}}
