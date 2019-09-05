from flask import Flask, render_template, g
import sqlite3
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, NumberRange
from datetime import time
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base

#creates the sqllite db 
engine = create_engine('sqlite:///C:\\sqlitedbs\\newschool.db', echo=True)
Base = declarative_base()


app = Flask(__name__)


class posts(Base):
	__tablename__ = "woot"
	id = Column(String, primary_key=True)
	title = Column(String(80), unique=True, nullable=False)
	link = Column(String(120), unique=True, nullable=False)
	category = Column(String(120), unique=True, nullable=False)
	date_added = Column(String(120), unique=False, nullable=False)
	thread_text = Column(String(400), unique=True, nullable=False)
	image = Column(String(400), unique=True, nullable=False)

# For support tickets
class ticket(Base):
	__tablename__ = "ticket"
	id = Column(String, primary_key=True)
	contact_name = Column(String(80), unique=False, nullable=False)
	description = Column(String(80), unique=False, nullable=False)
	version = Column(String(120), unique=False, nullable=True)
	priority = Column(String(120), unique=False, nullable=True)
	status = Column(String(120), unique=False, nullable=True)
	o365 = Column(String(400), unique=False, nullable=True)
	assigned_to = Column(String(400), nullable=True)

class TicketCreate(FlaskForm):
	cx_id = StringField('Customer ID', validators=[DataRequired()])
	contact_name = StringField('Contact Name', validators=[DataRequired()])
	description = TextAreaField('Description', validators=[DataRequired()])
	version = IntegerField('Version', validators=[NumberRange(min=2000,max=2020)])
	priority =  StringField('Priority')
	status =StringField('Status')
	o365 = BooleanField('Office 365')
	assigned_to = StringField('Assigned to', validators=[DataRequired()])
# end for support tickets
	
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)


#this is required. Similar to a "commit"
Base.metadata.create_all(engine)


#template for creating a table
# class School(Base):
#     __tablename__ = "woot"
#     id = Column(Integer, primary_key=True)
#     name = Column(String)  


# don't know what this does
#     def __init__(self, name):
#         self.name = name    




# Login form for index.html
class MyForm(FlaskForm):
    log_in_name = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

# Search fields for support tickets
class TicketSearch(FlaskForm):
	name = StringField('Name', validators=[DataRequired()])
	address = TextAreaField('Address', validators=[DataRequired()])
	cx_id = IntegerField('Customer ID', validators=[NumberRange(min=4000000000,max=4009999999)])
	order_num = IntegerField('Order Number', validators=[NumberRange(min=1000000000,max=1009999999)])






app = Flask(__name__)
app.debug = True

@app.teardown_appcontext
def close_db(error):
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()		

if __name__ == "__main__":
    app.run()

#Secrete key for WTF forms
WTF_CSRF_SECRET_KEY = 'a random string'
SECRET_KEY = "test"
app.config['SECRET_KEY'] = SECRET_KEY

#cd C:\Users\MGLafayette\Desktop\Projects\Undergrade Research Project
#env\Scripts\activate
#set FLASK_ENV=development
#py -m flask run

@app.route('/', methods=['GET', 'POST'])
def index():
	form = MyForm()
	WTF_CSRF_SECRET_KEY = 'a random string'
	return render_template('index.html', form=form)


@app.route('/submit', methods=('GET', 'POST'))
def submit():
    form = MyForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('submit.html', form=form)

@app.route('/ticket', methods=('GET', 'POST'))
def ticket():
    form = TicketSearch()
    return render_template('ticket.html', form=form)

@app.route('/createticket', methods=('GET', 'POST'))
def ticketcreate():
    form = TicketCreate()
    if form.validate_on_submit():
    	print (form.cx_id.data)
    	engine.execute('INSERT INTO ticket (id, contact_name, description, version, priority, status, o365, assigned_to) VALUES (?,?,?,?,?,?,?,?);', (form.cx_id.data, form.contact_name.data, form.description.data, form.version.data, form.priority.data, form.status.data, form.o365.data, form.assigned_to.data))
    	return render_template('createticket.html', form=form)
    return render_template('createticket.html', form=form)

@app.route('/createdb', methods=('GET', 'POST'))
def createdb():
	engine.execute('INSERT INTO ticket (id, description) VALUES ("2", "test");')
	return 'done'


#route for line graph
@app.route("/simple_chart")
def chart():
    legend = 'Clients Activated'
    labels = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "December"]
    values = [10, 9, 8, 7, 6, 4, 7, 8]
    return render_template('chart.html', values=values, labels=labels, legend=legend)

#pie chart
@app.route("/pie_chart")
def pie():
	activated = 6
	refused = 1
	no_answer = 4
	#probably want to use a dict for some of these values
	legend = 'Clients Activated'
	labels = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "December"]
	values = [10, 9, 8, 7, 6, 4, 7, 8]
	ac_label = "red"
	re_label = "yellow"
	no_label = "blue"
	return render_template('pie.html', values=values, labels=labels, legend=legend, activated=activated, refused=refused, no_answer=no_answer)