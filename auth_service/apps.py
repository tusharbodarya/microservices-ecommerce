# apps.py

from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/authdb"
app.config["JWT_SECRET_KEY"] = "7c1e8e5d2f8f4b7e8f1e2d3c4b5a6f7d8e9c0a1b2c3d4e5f6a7b8c9d0e1f2a3"

mongo = PyMongo(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

def initialize_db():
    return mongo, bcrypt, jwt

def register_user(username, password):
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = {
        "username": username,
        "password": hashed_password
    }
    mongo.db.users.insert_one(user)
    return user

def authenticate_user(username, password):
    user = mongo.db.users.find_one({"username": username})
    if user and bcrypt.check_password_hash(user['password'], password):
        return user
    return None
