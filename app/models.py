from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, Sequence, Boolean, Time
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import LoginManager, UserMixin
from app import db, login
from sqlalchemy import text

#####To create an actual table please use
# https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database #
# You will need to manually create the tables from the command line but will make future changes much easier as the app grows


##open admin cmd
#paste 
# cd C:\Program Files\MySQL\MySQL Server 8.0\bin
# mysqldump -e -uMatt -pElements1! -hlocalhost crm_system > C:\project.sql;


# Table for customers (when created)
#done

class Customer(db.Model):
	cx_id = db.Column(Integer, primary_key=True, auto_increment=True)
	company_name = db.Column(String(120), unique=False, nullable=False)
	customer_fname = db.Column(String(120), unique=False, nullable=True)
	customer_lname = db.Column(String(120), unique=False, nullable=True)
	city = db.Column(String(120), unique=False, nullable=True)
	state = db.Column(String(120), unique=False, nullable=True)
	address = db.Column(String(120), unique=False, nullable=True)
	zip_code = db.Column(String(120), unique=False, nullable=True)
	email = db.Column(String(120), unique=False, nullable=True)
	phone_num = db.Column(String(120), unique=False, nullable=True)
	valid_support = db.Column(String(120), unique=False, nullable=True)
	notes = db.Column(String(120), unique=False, nullable=True)

# For support tickets
#done
class Ticket(db.Model):
	id = db.Column(Integer, primary_key=True, autoincrement=True)
	contact_name = db.Column(String(80), unique=False, nullable=False)
	account_id = db.Column(Integer, unique=False, nullable=False)
	description = db.Column(String(80), unique=False, nullable=False)
	version = db.Column(String(120), unique=False, nullable=True)
	priority = db.Column(String(120), unique=False, nullable=True)
	status = db.Column(String(120), unique=False, nullable=True)
	o365 = db.Column(String(120), unique=False, nullable=True)
	o365status = db.Column(String(120), unique=False, nullable=True)
	valid_support = db.Column(Boolean, unique=False, nullable=True)
	assigned_to = db.Column(String(400), nullable=True)



#possibly done?
class User(db.Model, UserMixin):
	id = db.Column(Integer, primary_key=True)
	username = db.Column(String(64), index=True, unique=True)
	email = db.Column(String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	role = db.Column(db.String(15), index=True, unique=False)

	
	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '<User {}>'.format(self.username) 


class Time(db.Model):
	month = db.Column(String(120), primary_key=True, auto_increment=True)
	day = db.Column(String(120), primary_key=True, auto_increment=True)
	hour = db.Column(Time, primary_key=True, auto_increment=True)
	cx_id = db.Column(Integer, nullable=False)
	assigned_by = db.Column(Integer, nullable=False, auto_increment=True)

# for valid support do an if (current date) falls within valid_support_date range, then set this field to true

#done
class Invoice(db.Model):
	invoice_num = db.Column(Integer, primary_key=True, auto_increment=True)
	amount = db.Column(Integer, unique=False, nullable=False)
	description = db.Column(String(240), unique=False, nullable=False)
	date_created = db.Column(Date, unique=False, nullable=False)
	cx_id = db.Column(Integer, ForeignKey("customer.cx_id"), unique=True, nullable=False) 
	support_plan = db.Column(String(120), unique=False, nullable=True)
	sales_rep_id = db.Column(Integer, unique=False, nullable=False)
	valid_support_date = db.Column(Date, unique=False, nullable=False)

#done
class Support_Rep(db.Model):
	support_rep_id = db.Column(Integer, primary_key=True, auto_increment=True)
	support_first_name = db.Column(String(120), unique=False, nullable=False)
	support_last_name = db.Column(String(120), unique=False, nullable=False)

#https://www.mockaroo.com/
#C:\ProgramData\MySQL\MySQL Server 8.0\Data\crm_system
#start mysql
#disable secure option in my.ini
# LOAD DATA INFILE 'sales_rep.csv' 
# INTO TABLE sales__rep 
# FIELDS TERMINATED BY ',' 
# ENCLOSED BY '"'
# LINES TERMINATED BY '\n'
# IGNORE 1 ROWS;

# LOAD DATA INFILE 'customer.csv' 
# INTO TABLE customer 
# FIELDS TERMINATED BY ',' 
# ENCLOSED BY '"'
# LINES TERMINATED BY '\n'
# IGNORE 1 ROWS;

class Sales_Rep(db.Model):
	sales_rep_id = db.Column(Integer, primary_key=True, auto_increment=True)
	sales_first_name = db.Column(String(120), unique=False, nullable=False)
	sales_last_name = db.Column(String(120), unique=False, nullable=False)
	commission = db.Column(Integer, unique=False, nullable=False)


####The __repr__ method tells Python how to print objects of this class
#>>> from app.models import User
#>>> u = User(username='susan', email='susan@example.com')
#>>> u
#<User susan>

@login.user_loader
def load_user(id):
	return User.query.get(int(id))


#Base.metadata.create_all(engine)
 # In case user table doesn't exists already. Else remove it.    


try:
	db.create_all()
	db.commit()
	db.close()
except:
	print("database already exists")

try:
	sql = text('ALTER TABLE Customer AUTO_INCREMENT = 40000000')
	db.engine.execute(sql)

	sql = text('ALTER TABLE Invoice AUTO_INCREMENT = 10000000')
	db.engine.execute(sql)

	# https://stackoverflow.com/questions/30207493/sqlalchemy-orm-exc-flusherror-instance-has-a-null-identity-key
	sql = text('ALTER TABLE Ticket AUTO_INCREMENT = 80000000')
	db.engine.execute(sql)

	sql = text('ALTER TABLE Time AUTO_INCREMENT = 0')
	db.engine.execute(sql)

	sql = text('ALTER TABLE Support_Rep AUTO_INCREMENT = 90000000')
	db.engine.execute(sql)

	db.engine.commit()
	db.engine.close()
except:
	print("The alters failed")