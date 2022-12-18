#import required libraries
import flask
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy

#configure Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'

#create SQLAlchemy database object
db = SQLAlchemy(app)

#create database table
class users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    age = db.Column(db.Integer)

    def __init__(self,id,name,email,age):
        self.id = id
        self.name = name
        self.email = email
        self.age = age

class products(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(50))
    price = db.Column(db.Integer)

    def __init__(self,id,name,description,price):
        self.id = id
        self.name = name
        self.description = description
        self.price = price

class orders(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)

    def __init__(self,id,user_id,product_id,quantity):
        self.id = id
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity

#create endpoints
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = users(name=data['name'], email=data['email'], age=data['age'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message' : 'New user created!'})

@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    new_product = products(name=data['name'], description=data['description'], price=data['price'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message' : 'New product created!'})

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    new_order = orders(user_id=data['user_id'], product_id=data['product_id'], quantity=data['quantity'])
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'message' : 'New order created!'})

@app.route('/users', methods=['GET'])
def get_users():
    users = users.query.all()
    users_list = []
    for user in users:
        user_data = {}
        user_data['id'] = user.id
        user_data['name'] = user.name
        user_data['email'] = user.email
        user_data['age'] = user.age
        users_list.append(user_data)
    return jsonify({'users' : users_list})

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'message' : 'No user found!'})
    user_data = {}
    user_data['id'] = user.id
    user_data['name'] = user.name
    user_data['email'] = user.email
    user_data['age'] = user.age
    return jsonify({'user' : user_data})

@app.route('/products', methods=['GET'])
def get_products():
    products = products.query.all()
    products_list = []
    for product in products:
        product_data = {}
        product_data['id'] = product.id
        product_data['name'] = product.name
        product_data['description'] = product.description
        product_data['price'] = product.price
        products_list.append(product_data)
    return jsonify({'products' : products_list})

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = products.query.filter_by(id=product_id).first()
    if not product:
        return jsonify({'message' : 'No product found!'})
    product_data = {}
    product_data['id'] = product.id
    product_data['name'] = product.name
    product_data['description'] = product.description
    product_data['price'] = product.price
    return jsonify({'product' : product_data})

@app.route('/orders', methods=['GET'])
def get_orders():
    orders = orders.query.all()
    orders_list = []
    for order in orders:
        order_data = {}
        order_data['id'] = order.id
        order_data['user_id'] = order.user_id
        order_data['product_id'] = order.product_id
        order_data['quantity'] = order.quantity
        orders_list.append(order_data)
    return jsonify({'orders' : orders_list})

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = orders.query.filter_by(id=order_id).first()
    if not order:
        return jsonify({'message' : 'No order found!'})
    order_data = {}
    order_data['id'] = order.id
    order_data['user_id'] = order.user_id
    order_data['product_id'] = order.product_id
    order_data['quantity'] = order.quantity
    return jsonify({'order' : order_data})


#run the app
if __name__ == '__main__':
    app.run(debug=True)