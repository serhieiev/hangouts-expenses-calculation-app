from fastapi.testclient import TestClient
from src.main import app
from tests.conftest import test_db, mock_current_user

client = TestClient(app)

def test_list_hangouts_basic(test_db, mock_current_user):
    response = client.get("/hangouts/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_list_hangouts_pagination(test_db, mock_current_user):
    response = client.get("/hangouts/?skip=0&limit=2")
    assert response.status_code == 200
    assert len(response.json()) <= 2

def test_list_hangouts_no_data(test_db, mock_current_user):
    # Empty the test database or set up a scenario with no hangouts
    response = client.get("/hangouts/")
    assert response.status_code == 200
    assert response.json() == []
    # Add more assertions as needed

def test_list_hangouts_unauthorized():
    response = client.get("/hangouts/")
    assert response.status_code == 401
