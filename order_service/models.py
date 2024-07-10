from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
import pika
import json

def initialize_db(app):
    mongo = PyMongo(app)
    jwt = JWTManager(app)
    return mongo, jwt

def send_message(queue, message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_publish(exchange='', routing_key=queue, body=message)
    connection.close()

def create_order(mongo, user_id, product_id, quantity):
    order = {
        "user_id": user_id,
        "product_id": product_id,
        "quantity": quantity,
        "status": "created"
    }
    mongo.db.orders.insert_one(order)
    send_message('order_created', json.dumps(order))
    return order

def update_order(mongo, order_id, status):
    mongo.db.orders.update_one({"_id": order_id}, {"$set": {"status": status}})
    updated_order = mongo.db.orders.find_one({"_id": order_id})
    return updated_order
