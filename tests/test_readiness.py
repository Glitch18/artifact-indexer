# AI Contribution Weight: 100% AI Generated / 0% Human Refactored
"""Check dependency failure behavior and the skeleton's public API boundary."""

from unittest.mock import Mock

from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError

from app.main import app


def test_liveness_is_independent_of_database_and_business_routes_are_absent(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    with TestClient(app) as client:
        assert client.get("/healthz").json() == {
            "status": "ok",
            "service": "artifact-indexer",
            "phase": "week-1",
        }
        assert client.get("/healthz").status_code == 200
        assert client.get("/readyz").status_code == 503
        assert client.get("/api/v1/artifacts").status_code == 404


def test_database_failure_returns_503_without_driver_details(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    with TestClient(app) as client:
        engine = Mock()
        engine.connect.side_effect = OperationalError(
            "SELECT 1", {}, Exception("private DSN and driver details")
        )
        app.state.engine = engine
        response = client.get("/readyz")
        assert response.status_code == 503
        assert response.json() == {"detail": "Database unavailable"}
        assert client.get("/healthz").status_code == 200
