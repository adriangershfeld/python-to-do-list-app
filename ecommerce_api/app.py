from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
import os

# Initialize app
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@localhost/ecommerce_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database and Marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    email = db.Column(db.String(100), unique=True, nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

class OrderProduct(db.Model):
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)

# Marshmallow schemas
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product

# Initialize schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# CRUD Endpoints
# User Endpoints
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return users_schema.jsonify(users)

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)

@app.route('/users', methods=['POST'])
def create_user():
    name = request.json['name']
    address = request.json.get('address', None)
    email = request.json['email']

    new_user = User(name=name, address=address, email=email)
    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    user.name = request.json['name']
    user.address = request.json.get('address', user.address)
    user.email = request.json['email']

    db.session.commit()
    return user_schema.jsonify(user)

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User deleted'})

# Product Endpoints
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return products_schema.jsonify(products)

@app.route('/products/<id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)

@app.route('/products', methods=['POST'])
def create_product():
    product_name = request.json['product_name']
    price = request.json['price']

    new_product = Product(product_name=product_name, price=price)
    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)

@app.route('/products/<id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)
    product.product_name = request.json['product_name']
    product.price = request.json['price']

    db.session.commit()
    return product_schema.jsonify(product)

@app.route('/products/<id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()

    return jsonify({'message': 'Product deleted'})

# Order Endpoints
@app.route('/orders', methods=['POST'])
def create_order():
    user_id = request.json['user_id']
    order_date = datetime.strptime(request.json['order_date'], '%Y-%m-%d')

    new_order = Order(user_id=user_id, order_date=order_date)
    db.session.add(new_order)
    db.session.commit()

    return order_schema.jsonify(new_order)

@app.route('/orders/<order_id>/add_product/<product_id>', methods=['POST'])
def add_product_to_order(order_id, product_id):
    association = OrderProduct.query.filter_by(order_id=order_id, product_id=product_id).first()
    if association:
        return jsonify({'message': 'Product already in order'}), 400

    new_association = OrderProduct(order_id=order_id, product_id=product_id)
    db.session.add(new_association)
    db.session.commit()

    return jsonify({'message': 'Product added to order'})

@app.route('/orders/<order_id>/remove_product/<product_id>', methods=['DELETE'])
def remove_product_from_order(order_id, product_id):
    association = OrderProduct.query.filter_by(order_id=order_id, product_id=product_id).first()
    if not association:
        return jsonify({'message': 'Product not in order'}), 404

    db.session.delete(association)
    db.session.commit()

    return jsonify({'message': 'Product removed from order'})

@app.route('/orders/user/<user_id>', methods=['GET'])
def get_user_orders(user_id):
    orders = Order.query.filter_by(user_id=user_id).all()
    return orders_schema.jsonify(orders)

@app.route('/orders/<order_id>/products', methods=['GET'])
def get_order_products(order_id):
    associations = OrderProduct.query.filter_by(order_id=order_id).all()
    product_ids = [assoc.product_id for assoc in associations]
    products = Product.query.filter(Product.id.in_(product_ids)).all()
    return products_schema.jsonify(products)

# Run server
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
