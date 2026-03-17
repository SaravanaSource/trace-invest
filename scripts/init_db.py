"""Initialize the development database by creating tables.

Run from repository root:

    Set-Location trace-invest
    $env:PYTHONPATH='src'; & ..\.venv\Scripts\python.exe scripts/init_db.py

This is intentionally simple for local/dev use. For production use alembic migrations.
"""
from trace_invest.db import engine
from trace_invest.db.models import Base


def init_db():
    Base.metadata.create_all(bind=engine)
    print("Created DB tables (if not existing)")


if __name__ == '__main__':
    init_db()
