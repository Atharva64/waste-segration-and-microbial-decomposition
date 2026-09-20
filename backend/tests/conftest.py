import os

import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("DB_PASSWORD", "test-password")
os.environ.setdefault("DB_NAME", "waste_management")

from backend.app.database.session import get_db
from backend.app.main import app


@pytest.fixture
def client():
    app.dependency_overrides[get_db] = lambda: None

    with TestClient(
        app,
        raise_server_exceptions=False,
    ) as test_client:
        yield test_client

    app.dependency_overrides.clear()
