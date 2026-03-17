from celery import Celery
import os

BROKER = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")

celery_app = Celery("trace_invest_tasks", broker=BROKER, backend=BACKEND)
celery_app.conf.task_routes = {"trace_invest.tasks.alpha.run_alpha_pipeline": {"queue": "alpha"}}
# default schedule: run alpha pipeline once every day at 02:00 UTC (config via env)
from datetime import timedelta
import os

ALPHA_CRON = os.environ.get("ALPHA_PIPELINE_CRON", None)
if ALPHA_CRON:
	# allow user to provide Celery beat schedule as a simple cron expression (not parsed here)
	# For now fallback to periodic every 24h if ALPHA_PIPELINE_CRON is set but not supported.
	celery_app.conf.beat_schedule = {
		"alpha-daily": {
			"task": "trace_invest.tasks.alpha.run_alpha_pipeline",
			"schedule": timedelta(hours=24),
			"options": {"queue": "alpha"},
		}
	}
else:
	celery_app.conf.beat_schedule = {
		"alpha-daily": {
			"task": "trace_invest.tasks.alpha.run_alpha_pipeline",
			"schedule": timedelta(hours=24),
			"options": {"queue": "alpha"},
		}
	}

celery_app.conf.timezone = "UTC"
