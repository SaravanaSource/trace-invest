"""Initialize the database (temporary migration script).

This script creates tables using SQLAlchemy metadata. For production use,
replace with Alembic migrations.
"""
from trace_invest.db import engine
from trace_invest.db.models import Base


def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Done.")


if __name__ == '__main__':
    init_db()
