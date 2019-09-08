from app import app, db
from flask import Flask, render_template, flash, redirect, url_for, request
from config import Config
import sqlite3
from datetime import time
from flask_login import current_user, login_user
from app.models import User
from app.forms import RegistrationForm, TicketCreate, MyForm




#cd C:\Users\MGLafayette\Desktop\Projects\Undergrade Research Project
#env\Scripts\activate
#set FLASK_ENV=development
#py -m flask run

@app.route('/')
@app.route('/index')
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

#TEST
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)
#END TEST


@app.route('/ticket', methods=('GET', 'POST'))
def ticket():
    form = TicketSearch()
    return render_template('ticket.html', form=form)

@app.route('/createticket', methods=('GET', 'POST'))
def createticket():
    form = TicketCreate()
    if form.validate_on_submit():
    	print (form.cx_id.data)
    	engine.execute('INSERT INTO ticket (id, contact_name, description, version, priority, status, o365, assigned_to) VALUES (?,?,?,?,?,?,?,?);', (form.cx_id.data, form.contact_name.data, form.description.data, form.version.data, form.priority.data, form.status.data, form.o365.data, form.assigned_to.data))
    	return render_template('createticket.html', form=form)
    return render_template('createticket.html', form=form)

# @app.route('/createdb', methods=('GET', 'POST'))
# def createdb():
# 	engine.execute('INSERT INTO ticket (id, description) VALUES ("2", "test");')
# 	return 'done'


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