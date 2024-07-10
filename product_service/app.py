from flask import Flask, request, jsonify
from models import initialize_db, create_product, update_product
from flask_jwt_extended import JWTManager, jwt_required
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://mongo:27017/productdb"
app.config["JWT_SECRET_KEY"] = "7c1e8e5d2f8f4b7e8f1e2d3c4b5a6f7d8e9c0a1b2c3d4e5f6a7b8c9d0e1f2a3"

mongo, jwt = initialize_db(app)
limiter = Limiter(app, key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])

logging.basicConfig(level=logging.INFO)

@app.errorhandler(Exception)
def handle_exception(e):
    logging.error(f"An error occurred: {e}")
    return {"message": "Internal server error"}, 500

@app.route('/products', methods=['POST'])
@jwt_required()
@limiter.limit("10 per minute")
def create_product_route():
    data = request.get_json()
    product = create_product(mongo, data['name'], data['price'], data['quantity'])
    return jsonify(product), 201

@app.route('/products/<product_id>', methods=['PUT'])
@jwt_required()
@limiter.limit("10 per minute")
def update_product_route(product_id):
    data = request.get_json()
    product = update_product(mongo, product_id, data['name'], data['price'], data['quantity'], data['version'])
    if product:
        return jsonify(product), 200
    return jsonify({"message": "Product version mismatch or not found"}), 409

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
