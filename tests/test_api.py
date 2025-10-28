# Location: tests/test_api.py
import pytest

@pytest.mark.asyncio
async def test_health_check(client):
    """Test health check endpoint."""
    response = await client.get("/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "environment" in data

@pytest.mark.asyncio
async def test_echo_endpoint(client):
    """Test echo endpoint with valid input."""
    payload = {"message": "Hello, SupportGPT!"}
    response = await client.post("/v1/echo", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Hello, SupportGPT!"
    assert "id" in data
    assert "timestamp" in data

@pytest.mark.asyncio
async def test_echo_validation(client):
    """Test echo endpoint validation (empty message should fail)."""
    payload = {"message": ""}
    response = await client.post("/v1/echo", json=payload)
    assert response.status_code == 422  # Validation error
