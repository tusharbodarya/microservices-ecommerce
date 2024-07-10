import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_create_order(client):
    response = client.post('/orders', json={
        "user_id": "user1",
        "product_id": "product1",
        "quantity": 2
    })
    assert response.status_code == 201

def test_update_order(client):
    order_id = "some_id"
    response = client.put(f'/orders/{order_id}', json={
        "status": "shipped"
    })
    assert response.status_code == 200
