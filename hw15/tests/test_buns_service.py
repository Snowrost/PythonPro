import pytest
from fastapi.testclient import TestClient
from buns.service import app

client = TestClient(app)

def test_get_buns():
    response = client.get("/calculate_buns")
    assert response.status_code == 200
    data = response.json()
    assert "buns" in data
    assert data["buns"] == 2