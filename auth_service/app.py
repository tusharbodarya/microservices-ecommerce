from flask import Flask, request, jsonify
from models import initialize_db, register_user, authenticate_user
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://mongo:27017/authdb"
app.config["JWT_SECRET_KEY"] = "7c1e8e5d2f8f4b7e8f1e2d3c4b5a6f7d8e9c0a1b2c3d4e5f6a7b8c9d0e1f2a3"

mongo, bcrypt, jwt = initialize_db(app)
limiter = Limiter(app, key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])

logging.basicConfig(level=logging.INFO)

@app.errorhandler(Exception)
def handle_exception(e):
    logging.error(f"An error occurred: {e}")
    return {"message": "Internal server error"}, 500

@app.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    user = register_user(mongo, bcrypt, data['username'], data['password'])
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = authenticate_user(mongo, bcrypt, data['username'], data['password'])
    if user:
        access_token = create_access_token(identity=user['username'])
        return jsonify(access_token=access_token), 200
    return jsonify({"message": "Invalid credentials"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
