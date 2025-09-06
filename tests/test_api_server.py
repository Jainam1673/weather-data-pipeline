import pytest
from httpx import AsyncClient
try:
    from httpx import ASGITransport
except ImportError:
    ASGITransport = None  # Fallback for older httpx
from src.api.server import app


@pytest.mark.asyncio
async def test_health_endpoint(monkeypatch):
    class DummyResp:
        status_code = 200
        def json(self):
            return {}

    import src.api.server as server_mod
    monkeypatch.setattr(server_mod.requests, "get", lambda *args, **kwargs: DummyResp())

    transport = ASGITransport(app=app) if ASGITransport else None
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data.get("status") == "healthy"


@pytest.mark.asyncio
async def test_root_endpoint():
    transport = ASGITransport(app=app) if ASGITransport else None
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "Advanced Weather Data Pipeline" in data.get("message", "")

