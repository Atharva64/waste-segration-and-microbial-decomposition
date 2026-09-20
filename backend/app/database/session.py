from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.database.config import (
    DATABASE_URL
)


# ============================================================
# SQLAlchemy Engine
# ============================================================

engine = create_engine(
    DATABASE_URL,

    # Check stale/broken connections before use
    pool_pre_ping=True,

    # Display generated SQL when debugging.
    # Keep False normally.
    echo=False
)


# ============================================================
# Database Session Factory
# ============================================================

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False
)


# ============================================================
# FastAPI Database Dependency
# ============================================================

def get_db():
    """
    Provide one SQLAlchemy database session
    for a FastAPI request.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()