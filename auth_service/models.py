from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

def initialize_db(app):
    mongo = PyMongo(app)
    bcrypt = Bcrypt(app)
    jwt = JWTManager(app)
    return mongo, bcrypt, jwt

def register_user(mongo, bcrypt, username, password):
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = {
        "username": username,
        "password": hashed_password
    }
    mongo.db.users.insert_one(user)
    return user

def authenticate_user(mongo, bcrypt, username, password):
    user = mongo.db.users.find_one({"username": username})
    if user and bcrypt.check_password_hash(user['password'], password):
        return user
    return None
