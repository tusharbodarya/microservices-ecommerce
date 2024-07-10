from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager

def initialize_db(app):
    mongo = PyMongo(app)
    jwt = JWTManager(app)
    return mongo, jwt

def create_product(mongo, name, price, quantity):
    product = {
        "name": name,
        "price": price,
        "quantity": quantity,
        "version": 1
    }
    mongo.db.products.insert_one(product)
    return product

def update_product(mongo, product_id, name, price, quantity, version):
    product = mongo.db.products.find_one({"_id": product_id})
    if product and product['version'] == version:
        mongo.db.products.update_one(
            {"_id": product_id},
            {"$set": {"name": name, "price": price, "quantity": quantity, "version": version + 1}}
        )
        updated_product = mongo.db.products.find_one({"_id": product_id})
        return updated_product
    return None
