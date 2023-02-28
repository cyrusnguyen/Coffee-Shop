from cgitb import reset
from click import style
from flask_login import UserMixin
from . import db
from datetime import datetime, time

class User(db.Model, UserMixin):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)#should be 128 in length to store hash
    phone_number = db.Column(db.String(60), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    #image = db.Column(db.String(60), nullable=False, default='1.jpg')
    
    comments = db.relationship('Comment', backref='user')
    events = db.relationship('Event', backref='user')
    tickets = db.relationship('PurchasedTickets', backref='user')
    
    

    def __repr__(self):
        return "<Name: {}, id: {}>".format(self.name, self.id)

class Event(db.Model):
    __tablename__ = 'events'
    def defaultValue(column_name):
        def default_function(context):
            return context.current_parameters.get(column_name)
        return default_function

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    description = db.Column(db.String(500), nullable=False)
    image = db.Column(db.String(60), nullable=False, default='1.jpg') # this is going to be intresting
    price = db.Column(db.Float, nullable=False) # might cahnge to currency
    date_start = db.Column(db.Date, nullable=False)
    date_end = db.Column(db.Date, nullable=False)
    time_start =  db.Column(db.Time)
    time_end =  db.Column(db.Time)
    producer = db.Column(db.String(64), index=True)
    status = db.Column(db.String(64), index=True)
    style = db.Column(db.String(64), index=True)
    address = db.Column(db.String(64), index=True)
    city = db.Column(db.String(64), index=True)
    country = db.Column(db.String(64), index=True)
    ticketNo = db.Column(db.Integer, nullable=False)
    ticketLeft = db.Column(db.Integer, default=defaultValue('ticketNo'))
    


    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='event')
    tickets = db.relationship('PurchasedTickets', backref='event')

    def __repr__(self):
        return "<Name: {}, id: {}>".format(self.name, self.id)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    #add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))


    def __repr__(self):
        return "<Comment: {}>".format(self.text)

class PurchasedTickets(db.Model):
    __tablename__ = 'purchasedTickets'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)

    #add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))


    def __repr__(self):
        return '{}, {}'.format(self.event_id, self.id)



