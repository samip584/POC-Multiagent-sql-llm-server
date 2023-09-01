import pytest
from fastapi.testclient import TestClient
from app.app import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "app" in response.json()

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_ask_question():
    # Mock or skip if external deps
    pass  # Add proper test with mocking later