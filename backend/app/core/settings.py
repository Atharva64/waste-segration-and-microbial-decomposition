import os
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[3]

load_dotenv(PROJECT_ROOT / ".env")


DEFAULT_CORS_ORIGINS = (
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:4173",
    "http://127.0.0.1:4173",
)


def get_cors_origins() -> list[str]:
    """
    Browser origins allowed to call the API.

    Set CORS_ORIGINS in .env as a comma-separated list to override,
    for example: CORS_ORIGINS=https://waste-ai.example.com
    """

    raw_value = os.getenv("CORS_ORIGINS", "").strip()

    if not raw_value:
        return list(DEFAULT_CORS_ORIGINS)

    return [
        origin.strip().rstrip("/")
        for origin in raw_value.split(",")
        if origin.strip()
    ]
