import pytest
from flask import Flask
from flask_pymongo import PyMongo
from models import initialize_db, register_user, authenticate_user

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    app.config["MONGO_URI"] = "mongodb://localhost:27017/testdb"  # Use a separate test database
    initialize_db(app)
    
    @app.route('/auth/register', methods=['POST'])
    def register():
        data = {"username": "testuser", "password": "testpassword"}
        register_user(app.mongo, app.bcrypt, data['username'], data['password'])
        return {"message": "User registered successfully"}

    @app.route('/auth/login', methods=['POST'])
    def login():
        data = {"username": "testuser", "password": "testpassword"}
        user = authenticate_user(app.mongo, app.bcrypt, data['username'], data['password'])
        if user:
            return {"message": "Login successful"}
        else:
            return {"message": "Invalid credentials"}, 401
    
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_register_user(client):
    rv = client.post('/auth/register')
    assert rv.status_code == 200
    assert b'User registered successfully' in rv.data

def test_login_user(client):
    rv = client.post('/auth/login')
    assert rv.status_code == 200
    assert b'Login successful' in rv.data
