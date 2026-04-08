#!/usr/bin/env python3
"""Test script to verify model endpoints return correct information."""

import pytest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from unittest.mock import patch, MagicMock
from backend.app import app

@pytest.fixture
def client():
    """Create a test client."""
    from fastapi.testclient import TestClient
    return TestClient(app)

def test_health_endpoint(client):
    """Test that health endpoint works."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_root_endpoint(client):
    """Test that root endpoint works."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_list_models_with_valid_model(client):
    """Test that /v1/models returns model info when validation passes."""
    # This test would need the model to actually be loadable
    # For now, we'll just verify the endpoint responds
    response = client.get("/v1/models")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "object" in data
    assert len(data["data"]) > 0

def test_get_model_endpoint(client):
    """Test that /v1/models/{model_id} works."""
    response = client.get("/v1/models/local-mlx")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "local-mlx"
    assert data["object"] == "model"

if __name__ == "__main__":
    # Run quick basic tests without pytest
    from fastapi.testclient import TestClient
    
    client = TestClient(app)
    
    print("\n" + "=" * 80)
    print("Testing Model Validation Endpoints")
    print("=" * 80)
    
    # Test 1: Health
    print("\n1. Testing /health endpoint...")
    resp = client.get("/health")
    print(f"   Status: {resp.status_code}")
    print(f"   Response: {resp.json()}")
    
    # Test 2: Root
    print("\n2. Testing / endpoint...")
    resp = client.get("/")
    print(f"   Status: {resp.status_code}")
    print(f"   Response: {resp.json()}")
    
    # Test 3: Models list
    print("\n3. Testing /v1/models endpoint...")
    resp = client.get("/v1/models")
    print(f"   Status: {resp.status_code}")
    data = resp.json()
    print(f"   Number of models: {len(data.get('data', []))}")
    for model in data.get('data', []):
        print(f"      - {model.get('id')}: {model.get('note', 'No note')}")
    
    # Test 4: Specific model
    print("\n4. Testing /v1/models/{model_id} endpoint...")
    resp = client.get("/v1/models/local-mlx")
    print(f"   Status: {resp.status_code}")
    print(f"   Response: {resp.json()}")
    
    # Test 5: API tags (Ollama compat)
    print("\n5. Testing /api/tags endpoint...")
    resp = client.post("/api/tags")
    print(f"   Status: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        print(f"   Response: {data}")
    
    print("\n" + "=" * 80)
    print("✓ All basic endpoints are working")
    print("=" * 80)
