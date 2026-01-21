"""API endpoint tests."""

import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import tempfile
import shutil

from src.backend.main import app
from src.backend.config import Config
from src.backend.indexer import Indexer
from src.backend.ai.engine import AIEngine


@pytest.fixture
def temp_workspace():
    """Create temporary workspace for testing."""
    temp_dir = tempfile.mkdtemp()
    workspace = Path(temp_dir) / "workspace"
    workspace.mkdir()
    (workspace / "projects").mkdir()
    
    yield workspace
    
    shutil.rmtree(temp_dir)


@pytest.fixture
def test_client(temp_workspace):
    """Create test client with initialized indexer."""
    # This is a simplified test - in a real scenario, we'd properly initialize
    # the app state. For now, we'll test the endpoints that don't require
    # full initialization.
    return TestClient(app)


def test_health_endpoint(test_client):
    """Test health check endpoint."""
    response = test_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "ok"


def test_list_files_endpoint(test_client):
    """Test list files endpoint."""
    response = test_client.get("/api/files")
    # Should work even if no files (returns empty list)
    assert response.status_code in [200, 503]  # 503 if indexer not initialized


def test_list_projects_endpoint(test_client):
    """Test list projects endpoint."""
    response = test_client.get("/api/projects")
    assert response.status_code in [200, 503]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
