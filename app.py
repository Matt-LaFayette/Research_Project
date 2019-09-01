from flask import Flask, render_template, g
import sqlite3
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, NumberRange
from datetime import time

# Login form for index.html
class MyForm(FlaskForm):
    log_in_name = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

# Search fields for support tickets
class TicketSearch(FlaskForm):
	name = StringField('Name', validators=[DataRequired()])
	address = TextAreaField('Address', validators=[DataRequired()])
	cx_id = IntegerField('Customer ID', validators=[NumberRange(min=4000000000,max=4009999999)])

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