import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_register(client):
    response = client.post('/auth/register', json={
        "username": "testuser",
        "password": "testpass"
    })
    assert response.status_code == 201

def test_login(client):
    response = client.post('/auth/login', json={
        "username": "testuser",
        "password": "testpass"
    })
    assert response.status_code == 200
