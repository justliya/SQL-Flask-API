from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError
from sqlalchemy import String, select,ForeignKey, DateTime,Column,Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column,relationship
from datetime import datetime
from typing import List

# Initialize Flask app
app = Flask(__name__)

# MySQL database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Unstitch18@localhost/flask'
#Creating our Base Model
class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy and Marshmallow
db = SQLAlchemy(model_class=Base)
db.init_app(app)
ma = Marshmallow(app)


user_order = Table(
    'user_order',
    Base.metadata,
    Column('user_id', ForeignKey('users.id')),
    Column('order_id', ForeignKey('orders.id'))
)

order_product = Table(
    'order_product',
    Base.metadata,
    Column('order_id', ForeignKey('orders.id')),
    Column('product_id', ForeignKey('products.id'))
)

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str]= mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(30), nullable = False)
    email: Mapped[str] = mapped_column(String(100), unique= True)

    orders: Mapped[List["Order"]] = relationship("Order", secondary=user_order, back_populates="owner")
    

class Order(Base):
    __tablename__ = "orders"

    id:Mapped[int]= mapped_column(primary_key=True)
    order_date: Mapped[datetime] = mapped_column(DateTime, default=datetime, nullable=False)
    user_id: Mapped[int]= mapped_column(ForeignKey('users.id'))
    owner: Mapped[List["User"]] = relationship("User", secondary=user_order, back_populates="orders")
    products: Mapped[List["Product"]] = relationship("Product", secondary=order_product, back_populates="orders")


class Product(Base):
    __tablename__ = "products"

    id:Mapped[int]= mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(String(100), nullable= False)
    price: Mapped[float]= mapped_column(nullable= False)
    orders: Mapped[List["Order"]] = relationship("Order", secondary=order_product, back_populates="products")
    
#schemas

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
     model= User

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
     model= Product

class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
     model= Order

user_schema = UserSchema()
users_schema = UserSchema(many=True)   #allows for the serialization of a list of user objects

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)


#Endpoints  User

#Post/Create a user

@app.route('/users', methods=['POST'])

def create_user():
    try:
        user_data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_user = User(id=user_data['id'], address=user_data['address'], name=user_data['name'], email=user_data['email'])
    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user), 201

#Get/Retrieve all Users

@app.route('/users', methods=['GET'])
def get_users():

    query = select(User)
    users = db.session.execute(query).scalars().all() #Grabs and creates a list of users

    return users_schema.jsonify(users), 200  #Returns list of users to front end users

#Get/#Retrieve individual user by id

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = db.session.get(User, id)
    return user_schema.jsonify(user), 200

#Put/UPDATE individual user by id

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = db.session.get(User, id)

    if not user:
        return jsonify({"message": "Invalid user id"}), 400
    
    try:
        user_data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    user.address = user_data['address']
    user.name = user_data['name']
    user.email = user_data['email']

    db.session.commit()
    return user_schema.jsonify(user), 200

#Delete a user by ID

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = db.session.get(User, id)

    if not user:
        return jsonify({"message": "Invalid user id"}), 400
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"succefully deleted user {id}"}), 200

#Endpoint product

#Post/Create a new product

@app.route('/products', methods=['POST'])

def create_product():
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_product = Product(id=product_data['id'], product_name=product_data['product_name'], price=product_data['price'])
    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product), 201

#Get/Retrieve all products

@app.route('/products', methods=['GET'])
def get_products():
    query = select(Product)
    products = db.session.execute(query).scalars().all()

    return products_schema.jsonify(products), 200

#Get/Retrieve products by ID

@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = db.session.get(Product, id)
    return product_schema.jsonify(product), 200

#Put/Update a product by ID

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = db.session.get(Product, id)

    if not product:
        return jsonify({"message": "Invalid product id"}), 400

    try:
        product_data = product_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    product.product_name = product_data['product_name']
    product.price = product_data['price']

    db.session.commit()
    return product_schema.jsonify(product), 200

#Delete a product

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = db.session.get(Product, id)

    if not product:
        return jsonify({"message": "Invalid user id"}), 400
    
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": f"succefully deleted product {id}"}), 200


#Endpoint Order

#Post/Create orders

@app.route('/orders', methods=['POST'])

def create_order():
    try:
        order_data = order_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_order = Order(user_id=order_data['user_id'], order_date=order_data['order_date'])
    db.session.add(new_order)
    db.session.commit()

    return order_schema.jsonify(new_order), 201

#Get/Add products to an order

@app.route('/orders/<int:order_id>/add_product/<int:product_id>', methods=['POST'])
def add_orders(order_id, product_id):
    # Check if the order exists
    order = db.session.get(Order, order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404

    # Check if the product exists
    product = db.session.get(Product, product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    # Prevent duplicate products in the order
    if product in order.products:
        return jsonify({"error": "Product already in the order"}), 400

    # Add the product to the order
    order.products.append(product)
    db.session.commit()

    return jsonify({"message": f"Product {product.id} has been added to Order {order.id}!"}), 200


    
#Get/Add multiple orders to a user

@app.route('/orders/user/<int:user_id>', methods=['GET'])
def get_user_orders(user_id):
    # Assuming you have a User and Order relationship properly defined in your database models
    query = select(Order).where(Order.user_id == user_id)
    orders = db.session.execute(query).scalars().all()
    
    return orders_schema.jsonify(orders), 200

#GET all orders

@app.route('/orders/<int:order_id>/products', methods=['GET'])
def get_order_products(order_id):
    order = db.session.get(Order, order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404

    return products_schema.jsonify(order.products), 200

#Delete orders

@app.route('/orders/<int:id>/remove_product', methods=['DELETE'])
def delete_order(id):
    order = db.session.get(Order, id)

    if not order:
        return jsonify({"message": "Invalid user id"}), 400
    
    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": f"succefully deleted order{id}"}), 200



   
if __name__ == "__main__":

    with app.app_context():
        
      db.create_all()

    app.run(debug=True)