from cgitb import reset
from click import style
from flask_login import UserMixin
from . import db
from datetime import datetime, time
import json
from flask_login import AnonymousUserMixin

class User(db.Model, UserMixin):
    __tablename__='users'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, index=True, nullable=False)
    email = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)#should be 128 in length to store hash
    phone_number = db.Column(db.String(60), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(60), nullable=False, default='user.svg')
    role = db.Column(db.String(60), nullable=False, default='user')
    
    comments = db.relationship('Comment', backref='users')
    carts = db.relationship('Cart', backref='carts')
    

    def get_id(self):
        return (self.user_id)
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    # def __repr__(self):
    #     return "<Name: {}, user_id: {}>".format(self.name, self.user_id)

class Anonymous(AnonymousUserMixin):
  def __init__(self):
    self.name = 'Guest'
    self.user_id = 'Guest'
    
class Product(db.Model):
    __tablename__ = 'products'
    def defaultValue(column_name):
        def default_function(context):
            return context.current_parameters.get(column_name)
        return default_function
    
    

    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(64), nullable=False, default='1.jpg')
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.String(10), nullable=False) 
    sold_quantity = db.Column(db.Integer, nullable=False, default=0) 
    released_date = db.Column(db.Date, nullable=False, default=datetime.today()) 

    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'))
    comment = db.relationship('Comment', backref='products')
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.cart_id'))
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    # def __repr__(self):
    #     return "<Name: {}, product_id: {}>".format(self.name, self.product_id)
    
class CartProduct(db.Model):
    __tablename__ = 'cartProducts'

    
    cart_product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    price = db.Column(db.Float, nullable=False, default=0)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    total = db.Column(db.Float, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    modified_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    cart_id = db.Column(db.Integer, db.ForeignKey('carts.cart_id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))
   
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Category(db.Model):
    __tablename__ = 'categories'
    
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    description = db.Column(db.String(500), nullable=False)

    products = db.relationship('Product', backref='categories')

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return "<Name: {}, category_id: {}>".format(self.name, self.category_id)
    
class Comment(db.Model):
    __tablename__ = 'comments'
    comment_id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    #add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return "<Comment: {}>".format(self.text)

class ContactUs(db.Model):
    __tablename__ = 'contactus'
    contact_us_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(50))
    message = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return "<Comment: {}>".format(self.text)
    
class Cart(db.Model):
    __tablename__ = 'carts'
    cart_id = db.Column(db.Integer, primary_key=True)
    subtotal = db.Column(db.Float, nullable=False)
    total_quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    delivery_address = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phoneNo = db.Column(db.String(50), nullable=False)

    #add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    cart_products = db.relationship('CartProduct', backref='carts')

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return '{}, of user {}'.format(self.cart_id, self.user_id)



