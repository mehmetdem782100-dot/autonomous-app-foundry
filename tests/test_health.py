import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_health_check(async_client: AsyncClient):
    response = await async_client.get("/health")
    assert response.status_code in [200, 503]
    data = response.json()
    assert "api" in data
    assert data["api"] == "healthy"
