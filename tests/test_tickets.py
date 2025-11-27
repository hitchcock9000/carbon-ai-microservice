import pytest
from fastapi.testclient import TestClient
from src.api.main import app
from unittest.mock import patch, MagicMock, AsyncMock
import os

client = TestClient(app)

# Mock environment variables
@pytest.fixture(autouse=True)
def mock_env_vars():
    with patch("src.api.tickets.GITHUB_TOKEN", "test_token"), \
         patch("src.api.tickets.GITHUB_REPO", "test/repo"):
        yield

@pytest.fixture
def mock_github_response():
    return {
        "number": 123,
        "title": "Test Ticket",
        "body": "Test Description",
        "state": "open",
        "labels": [{"name": "priority:high"}, {"name": "category:bug"}],
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-01T00:00:00Z",
        "html_url": "http://github.com/test/repo/issues/123"
    }

@patch("src.api.tickets.httpx.AsyncClient")
def test_create_ticket(mock_client_cls, mock_github_response):
    mock_client = AsyncMock()
    mock_client_cls.return_value.__aenter__.return_value = mock_client
    
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = mock_github_response
    mock_client.post.return_value = mock_response

    response = client.post(
        "/api/v1/tickets/",
        json={
            "title": "Test Ticket",
            "description": "Test Description",
            "priority": "high",
            "category": "bug"
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == "123"
    assert data["title"] == "Test Ticket"
    assert data["priority"] == "high"

@patch("src.api.tickets.httpx.AsyncClient")
def test_list_tickets(mock_client_cls, mock_github_response):
    mock_client = AsyncMock()
    mock_client_cls.return_value.__aenter__.return_value = mock_client
    
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [mock_github_response]
    mock_client.get.return_value = mock_response

    response = client.get("/api/v1/tickets/")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == "123"

@patch("src.api.tickets.httpx.AsyncClient")
def test_get_ticket(mock_client_cls, mock_github_response):
    mock_client = AsyncMock()
    mock_client_cls.return_value.__aenter__.return_value = mock_client
    
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_github_response
    mock_client.get.return_value = mock_response

    response = client.get("/api/v1/tickets/123")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "123"

@patch("src.api.tickets.httpx.AsyncClient")
def test_update_ticket(mock_client_cls, mock_github_response):
    mock_client = AsyncMock()
    mock_client_cls.return_value.__aenter__.return_value = mock_client
    
    # Setup for get_github_issue (called internally)
    mock_get_response = MagicMock()
    mock_get_response.status_code = 200
    mock_get_response.json.return_value = mock_github_response
    
    # Setup for patch
    mock_patch_response = MagicMock()
    mock_patch_response.status_code = 200
    updated_response = mock_github_response.copy()
    updated_response["state"] = "closed"
    mock_patch_response.json.return_value = updated_response
    
    # Configure side_effect to return get_response first, then patch_response
    mock_client.get.return_value = mock_get_response
    mock_client.patch.return_value = mock_patch_response

    response = client.patch(
        "/api/v1/tickets/123",
        json={"status": "closed"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "closed"
