from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

def initialize_db(app):
    mongo = PyMongo(app)
    return mongo

def register_user(mongo, username, password):
    hashed_password = generate_password_hash(password)
    user = {
        "username": username,
        "password": hashed_password
    }
    mongo.db.users.insert_one(user)
    return user

def authenticate_user(mongo, username, password):
    user = mongo.db.users.find_one({"username": username})
    if user and check_password_hash(user['password'], password):
        return user
    return None
