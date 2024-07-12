from flask import Flask, request, jsonify
from models import initialize_db, create_order, update_order
from flask_jwt_extended import JWTManager, jwt_required
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/orderdb"
app.config["JWT_SECRET_KEY"] = "7c1e8e5d2f8f4b7e8f1e2d3c4b5a6f7d8e9c0a1b2c3d4e5f6a7b8c9d0e1f2a3"

mongo, jwt = initialize_db(app)
limiter = Limiter(app, key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])

logging.basicConfig(level=logging.INFO)

@app.errorhandler(Exception)
def handle_exception(e):
    logging.error(f"An error occurred: {e}")
    return {"message": str(e)}, 500

@app.route('/orders', methods=['POST'])
@jwt_required()
@limiter.limit("10 per minute")
def create_order_route():
    data = request.get_json()
    order = create_order(mongo, data['user_id'], data['product_id'], data['quantity'])
    return jsonify(order), 201

@app.route('/orders/<order_id>', methods=['PUT'])
@jwt_required()
@limiter.limit("10 per minute")
def update_order_route(order_id):
    data = request.get_json()
    order = update_order(mongo, order_id, data['status'])
    return jsonify(order), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
