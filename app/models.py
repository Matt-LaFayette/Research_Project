from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import LoginManager
from app import db, login

#####To create an actual table please use
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database #
# You will need to manually create the tables from the command line but will make future changes much easier as the app grows


# For support tickets
class Ticket(db.Model):
 	id = db.Column(String, primary_key=True)
 	contact_name = db.Column(String(80), unique=False, nullable=False)
 	description = db.Column(String(80), unique=False, nullable=False)
 	version = db.Column(String(120), unique=False, nullable=True)
 	priority = db.Column(String(120), unique=False, nullable=True)
 	status = db.Column(String(120), unique=False, nullable=True)
 	o365 = db.Column(String(400), unique=False, nullable=True)
 	assigned_to = db.Column(String(400), nullable=True)

class User(db.Model):
    id = db.Column(Integer, primary_key=True)
    username = db.Column(String(64), index=True, unique=True)
    email = db.Column(String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))


# Table for customers (when created)
class Customer(db.Model):
    cx_id = db.Column(Integer, primary_key=True)
    customer_name = db.Column(String(120), unique=False, nullable=True)
    city = db.Column(String(120), unique=False, nullable=True)
    state = db.Column(String(120), unique=False, nullable=True)
    address = db.Column(String(120), unique=False, nullable=True)
    zip_code = db.Column(String(120), unique=False, nullable=True)
    email = db.Column(String(120), unique=False, nullable=True)
    phone_num = db.Column(String(120), unique=False, nullable=True)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username) 

####The __repr__ method tells Python how to print objects of this class
#>>> from app.models import User
#>>> u = User(username='susan', email='susan@example.com')
#>>> u
#<User susan>

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

#Base.metadata.create_all(engine)