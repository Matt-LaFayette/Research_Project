from flask_wtf import FlaskForm
from flask_login import LoginManager, current_user, login_user
from wtforms import StringField, PasswordField, IntegerField, TextAreaField, BooleanField, SubmitField, SelectField, DateField, DateTimeField
from wtforms.validators import ValidationError, DataRequired, NumberRange, Email, EqualTo, Regexp, Optional
from app.models import User

class CreateCustomer(FlaskForm):
	customer_fname = StringField('First Name', validators=[DataRequired()])
	customer_lname = StringField('Last Name', validators=[DataRequired()])
	company_name = StringField('Company Name', validators=[DataRequired()])
	city = StringField('City', validators=[DataRequired()])
	state = StringField('State', validators=[DataRequired()])
	address = TextAreaField('Address', validators=[DataRequired()])
	zip_code = StringField('Zip', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired()])
	phone_num = StringField('Phone Number', validators=[DataRequired()])

# Form to create a support ticket
class TicketCreate(FlaskForm):
	cx_id = StringField('Customer ID', validators=[DataRequired(), Regexp('\d+',  message="Username must contain only letters numbers or underscore")])
	contact_name = StringField('Contact Name', validators=[DataRequired()])
	description = TextAreaField('Description', validators=[DataRequired()])
	version = IntegerField('Version', validators=[NumberRange(min=2000,max=2020)])
	priority =  SelectField(choices=[('high', 'High'), ('normal', 'Normal'), ('low', 'Low')])
	status = SelectField(choices=[('open', 'Open'), ('closed', 'Closed'), ('wip', 'Work In Progress'), ('pending', 'Fix Pending')])
	o365 = BooleanField('Office 365')
	o365status = SelectField(choices=[('onboarded', 'Onboarded'), ('no_contact', 'No Contact'), ('badinfo', 'Incorrect contact number'), ('Doesnt_want', 'Does not want')])
	assigned_to = StringField('Assigned to', validators=[DataRequired()])

# Login form for index.html
class MyForm(FlaskForm):
    log_in_name = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

#for customer invoices
class Invoice(FlaskForm):
	invoice_num = IntegerField('Invoice Number', validators=[NumberRange(min=100000000,max=100999999)])
	amount = IntegerField('Amount', validators=[DataRequired()])
	date_created = DateField('Date', format='%m-%d-%Y')
	cx_id = IntegerField('Customer ID', validators=[DataRequired()])
	support_plan = BooleanField('Valid Support?')
	sales_rep_id = IntegerField('Sales Rep ID')
	valid_support_date = DateField('Support Vaid Through', format='%m-%d-%Y')

class ApptDate(FlaskForm):
	date_input = DateTimeField(format='%Y-%m-%d %H:%M:%S')


# Search fields for support tickets
class TicketSearch(FlaskForm):
	name = StringField('Name', validators=[DataRequired()])
	address = TextAreaField('Address', validators=[DataRequired()])
	cx_id = IntegerField('Customer ID', validators=[NumberRange(min=4000000000,max=4009999999)])
	order_num = IntegerField('Order Number', validators=[NumberRange(min=1000000000,max=1009999999)])


# Search fields for customer
class SearchCustomer(FlaskForm):
	customer_fname = StringField('First Name', validators=[Optional()])
	customer_lname = StringField('Last Name', validators=[Optional()])
	city = StringField('City', validators=[DataRequired()])
	state = StringField('State', validators=[DataRequired()])
	address = TextAreaField('Address', validators=[Optional()])
	zip_code = StringField('Zip', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired()])
	phone_num = StringField('Phone Number', validators=[DataRequired()])
	cx_id = IntegerField('Customer ID', validators=[NumberRange(min=400000000,max=400999999), Optional()])

#Form to register a new username and password
class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	role = SelectField(choices=[('sales', 'Sales'), ('support', 'Support'), ('manager', 'Manager')])
	submit = SubmitField('Register')

	# def validate_username(self, username):
	# 	user = User.query.filter_by(username=username.data).first()
	# 	if user is not None:
	# 		raise ValidationError('Please use a different username.')

	# def validate_email(self, email):
	# 	user = User.query.filter_by(email=email.data).first()
	# 	if user is not None:
	# 		raise ValidationError('Please use a different email address.')