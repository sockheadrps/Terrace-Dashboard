from main import app
from httpx import AsyncClient
from fastapi.testclient import TestClient
import pytest


client = TestClient(app)


@pytest.mark.anyio
async def test_dashboard_endpoint():
    """
    Assertion 1: Tests the successful delivery of the /stats endpoint
    """
    async with AsyncClient(app=app, base_url="http://localhost") as ac:
        print(app.route)
        response = await ac.get("/dashboard")
        assert response.status_code == 200
