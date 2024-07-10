import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_create_product(client):
    response = client.post('/products', json={
        "name": "Product1",
        "price": 100,
        "quantity": 10
    })
    assert response.status_code == 201

def test_update_product(client):
    product_id = "some_id"
    response = client.put(f'/products/{product_id}', json={
        "name": "Product1",
        "price": 150,
        "quantity": 20,
        "version": 1
    })
    assert response.status_code == 200
