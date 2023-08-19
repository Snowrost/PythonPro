import pytest
from fastapi.testclient import TestClient
from ingridients.service import app

client = TestClient(app)

def test_get_ingredient():
    response = client.get("/ingredients/flour")
    assert response.status_code == 200
    data = response.json()
    assert data["ingredient_name"] == "flour"
    assert "quantity" in data

def test_get_all_ingredients():
    response = client.get("/ingredients")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)

def test_get_nonexistent_ingredient():
    response = client.get("/ingredients/owl")
    assert response.status_code == 200
    data = response.json()
    assert data["ingredient_name"] == "owl"
    assert data["quantity"] == 0