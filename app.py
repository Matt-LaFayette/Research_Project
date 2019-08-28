from flask import Flask, render_template, g
import sqlite3
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


class MyForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

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
#python -m flask run

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