import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import URL


# ============================================================
# Environment Configuration
# ============================================================

PROJECT_ROOT = Path(
    __file__
).resolve().parents[3]

ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(
    ENV_FILE
)


# ============================================================
# Database Settings
# ============================================================

DB_HOST = os.getenv(
    "DB_HOST",
    "localhost"
)

DB_PORT = int(
    os.getenv(
        "DB_PORT",
        "5432"
    )
)

DB_NAME = os.getenv(
    "DB_NAME",
    "waste_management"
)

DB_USER = os.getenv(
    "DB_USER",
    "postgres"
)

DB_PASSWORD = os.getenv(
    "DB_PASSWORD"
)


# ============================================================
# Validation
# ============================================================

if not DB_PASSWORD:
    raise RuntimeError(
        "DB_PASSWORD is not configured. "
        "Add it to the project .env file."
    )


# ============================================================
# SQLAlchemy Database URL
# ============================================================

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME
)