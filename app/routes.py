from app import app, db
from flask import Flask, render_template, flash, redirect, url_for, request, session
from config import Config
from datetime import time
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from app.models import User, Ticket, Customer, Time, Sales_Rep
from app.forms import RegistrationForm, TicketCreate, MyForm, TicketSearch, CreateCustomer, SearchCustomer, Invoice, ApptDate
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from sqlalchemy import text
from calendar import *
import datetime
from sqlalchemy import create_engine


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'

now = datetime.datetime.now()
month = int(now.month)
year = int(now.year)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


customer = ""

try:
	testtime = Time.query.all()
	#print (testtime)
except:
	print("I failed to query time")

#cd C:\Users\MGLafayette\Desktop\Projects\Undergrade Research Project
#env\Scripts\activate
#set FLASK_ENV=development
#py -m flask run

def get_db():
	db.session()

@app.teardown_appcontext
def close_db(error):
	db.session.close()
	db.session.remove()


@app.route('/')
@app.route('/index', methods=('GET', 'POST'))
def index():
	form = MyForm()
	get_db()
	WTF_CSRF_SECRET_KEY = 'a random string'
	if form.validate_on_submit():
		print("Query")
		user = User.query.filter_by(username=form.log_in_name.data).first()
		if user:
			print("found user")
			if check_password_hash(user.password_hash, form.password.data):
				login_user(user, remember=True)
				return redirect(url_for('createticket'))

		return '<h1>Invalid username or password</h1>'
	return render_template('index.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/create')
def create():
    db.create_all()
    return redirect(url_for('index'))


@app.route('/submit', methods=('GET', 'POST'))
def submit():
	form = MyForm()
	if form.validate_on_submit():
		return redirect('/success')
	return render_template('submit.html', form=form)

@app.route('/template', methods=('GET', 'POST'))
def template():
	#https://pythonhosted.org/Flask-Session/
	#will probably need to add this
	user = User.query.filter_by(username=current_user.username)
	print(current_user.username)
	month = int(now.month)
	print (month)
	try:
		test = session['id']
		cx_info = Customer.query.filter_by(cx_id=test)
	except:
		test = "broken"
		print ("i broke")
	customer = ""
	try:
		for x in cx_info:
			print ("I'm printing")
			print (x.cx_id)
			print (x.customer_name)
	except:
		print("I failed to print customer name")
	for y in user:
		print (y.role)
	return render_template('template.html', month=month, user=user, cx_info=cx_info, test=str(test))

#TEST
@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data, role=form.role.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Congratulations, you are now a registered user!')
		return redirect(url_for('index'))
	return render_template('register.html', title='Register', form=form)
#END TEST

@app.route('/salesorder', methods=('GET', 'POST'))
@login_required
def salesorder():
	form = Invoice()
	title = 'New Order'
	print(month)
	user = User.query.filter_by(username=current_user.username)
	return render_template('salesorder.html', month=month, user=user, title=title, form=form)


@app.route('/ticket', methods=('GET', 'POST'))
@login_required
def ticket():
	user = User.query.filter_by(username=current_user.username)
	form = TicketSearch()
	return render_template('ticket.html', user=user, form=form)

@app.route('/createcustomer', methods=('GET', 'POST'))
@login_required
def createcustomer():
	form = CreateCustomer()
	user = User.query.filter_by(username=current_user.username)
	title = 'Customer'
	return render_template('createcustomer.html', user=user, title=title, form=form)

@app.route('/mytickets', methods=('GET', 'POST'))
@login_required
def mytickets():
	title = "My Tickets"
	ticket = Ticket.query.filter_by(assigned_to=current_user.username)
	return render_template("mytickets.html", ticket=ticket)


@app.route('/listticket', methods=('GET', 'POST'))
@login_required
def listticket():
	user = User.query.filter_by(username=current_user.username)
	try:
		if session['name']:
			name = session['name']
			title = 'Tickets for ' + name
		else:
			title = "Error"
		ticket = Ticket.query.filter_by(account_id=session['id'])
	except:
		print("I've failed to list ticket")
		ticket = ""
		title = "Error"
	return render_template('listticket.html', user=user, title=title, ticket=ticket)

@app.route('/searchcustomer', methods=('GET', 'POST'))
@login_required
def searchcustomer():
	form1 = SearchCustomer()
	user = User.query.filter_by(username=current_user.username)
	title = "Search"
	return render_template('searchcustomer.html', user=user, title=title, form1=form1)

#this route is linked to searchcustomer and displays the results found
@app.route('/findaccount', methods=('GET', 'POST'))
@login_required
def findaccount():
	title = "Find Account"
	form = SearchCustomer()
	# print (session['response'])
	customerid = form.cx_id.data
	customerfname = form.customer_fname.data
	customerlname = form.customer_lname.data
	#Need to input logic so if someone enters name, then it then does a query to pull up the id by their name
	cxbyid = Customer.query.filter_by(cx_id=customerid)
	# if customerfname:
	# 	cxbyname = Customer.query.filter_by(customer_fname=customername)
	# if customerlname:
	# 	cxbyname = Customer.query.filter_by(customer_lname=customername)
	if form.validate_on_submit():
		x = 1
		for customer in cx:
			select = str(x) + 'Select'
			print ("Im' printing " + select)
			st = str(select)
			print ("Im' printing " + st)
			# selection = request.form.get(st)
			# print (selection)
			x = x + 1
			print(type(st))
			# session['name'] = customer.customer_name
			if st == 'Select':
				print("success")
	return render_template('findaccount.html', cxbyid=cxbyid, title=title)



@app.route('/test', methods=('GET', 'POST'))
def test():
	form = CreateCustomer()
	customer = Customer(customer_name=form.customer_name.data, company_name=form.company_name.data, city=form.city.data, state=form.state.data, address=form.address.data, zip_code=form.zip_code.data, email=form.email.data, phone_num=form.phone_num.data)
	try:
		db.session.add(customer)
		db.session.commit()
	except IntegrityError:
		db.session.rollback()
		return 'I failed and rolled back'
	# x = request.form['temptest']
	cx = Customer.query.filter_by(customer_name=form.customer_name.data).all()
	# session['response']= x
	# for x in cx:
	# 	print(x.cx_id)
	return render_template('test.html', test=test, customer=cx)

@app.route('/new', methods=('GET', 'POST'))
def new():
	return render_template('new.html')


@app.route('/createticket', methods=('GET', 'POST'))
@login_required
def createticket():
	form = TicketCreate()
	title = 'Ticket'
	user = User.query.filter_by(username=current_user.username)
	if request.method == 'POST':
		try:
			acctid = request.form['cx_id']
			acctname = request.form['cx_name']
			sql = text('ALTER TABLE Ticket AUTO_INCREMENT = 80000000')
			db.engine.execute(sql)
			db.session.commit()
			ticket = Ticket(account_id=acctid, contact_name=acctname, description=form.description.data, version=form.version.data, priority=form.priority.data, status=form.status.data, o365=form.o365.data, o365status=form.o365status.data, assigned_to=form.assigned_to.data)
			db.session.add(ticket)
			t = Ticket.query.all()
			for x in t:
				print (x.id)
			db.session.commit()
		except:
			print("I failed during create ticket")
	return render_template('createticket.html', month=month, user=user, title=title, form=form)


@app.route("/masterlist")
@login_required
def masterlist():
	try:
		customer = Customer.query.all()
		ticket = Ticket.query.all()
		user = User.query.all()
		sales = Sales_Rep.query.all()
		for x in ticket:
			print(x.id)
	except:
		print("I failed the masterlist")
		user = ""
		customer = ""
		ticket = ""
		sales = ""
	return render_template('masterlist.html', sales=sales, user=user, customer=customer, ticket=ticket)

@app.route("/selectcustomer/<id>")
def selectcustomer(id):
	session['id'] = id
	cx_info = Customer.query.filter_by(cx_id=session['id'])
	try:
		appt_info = Time.query.filter_by(cx_id= session['id'])
		for x in appt_info:
			session['month'] = x.month
			session['day'] = x.day
			session['hour'] = x.hour
	except:
		print("time query failed")
	for x in cx_info:
		session['name'] = x.customer_fname
		session['phone_num'] = x.phone_num
	try:
		print("session id")
		print(session['id'])
	except:
		print("I failed")
	return "nothing"

@app.route("/clearsession")
def clearsession():
	session.pop('id', None)
	session.pop('name', None)
	try:
		print(session['id'])
	except:
		print("I failed")
	return "nothing"

@app.route("/calendar/<month>", methods=('GET', 'POST'))
def calendar(month):
	testtime = ""
	form = ApptDate()
	user = User.query.filter_by(username=current_user.username)
	dt = datetime.datetime.now()
	yyyy = dt.year

	try:
		#testtime = Time.query.order_by('hour').all()
		#####Need to change
		#testtime = []
		sqlquery = text("SELECT month, day, date_format(hour, '%l%p') from time;")
		sql = db.engine.execute(sqlquery)
		testtime = sql.fetchall()
		for x in testtime:
			print (x)
	except:
		print("unable to query time")
	print (testtime)
	# num_days = monthrange(2019, 2)[1] # num_days = 28
	# print(num_days)
	tc= HTMLCalendar(firstweekday=6)
	cal = tc.formatmonth(int(year), int(month))
	# might not need
	try:
		print(request.form.get('appt'))
		timeadd = str(request.form.get('appt'))
		print(type(timeadd))
		print("insert")
		time = Time(month=10, day=4,hour=timeadd)
		c = calendar.TextCalendar(calendar.SUNDAY)
		strcal = c.formatmonth(2025,1)
		# sql = text("INSERT INTO time (hour) VALUES (%s)", (timeadd))
		print("attempting to execute")
		db.session.add(time)
		print("commit")
		db.session.commit()
		print("attempting to add")
		print("adding to db")
		print("committing...")
	except:
		print("I failed to grab the appt form")
	try:
		print(form.date_input.data)
	except:
		print("failed to get date input")
	return render_template('calendar.html', form=form, month=month, user=user, cal=cal, testtime=testtime)


#route for line graph
@app.route("/simple_chart")
@login_required
def chart():
	legend = 'Clients Activated'
	labels = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "December"]
	values = [10, 9, 8, 7, 6, 4, 7, 8]
	return render_template('chart.html', values=values, labels=labels, legend=legend)

#pie chart
#select s.sales_first_name, count(tic.id) from time t
#join ticket tic
#on t.cx_id = tic.account_id
#join sales__rep s 
#on s.sales_rep_id = t.assigned_by
#where tic.o365status = "onboarded"
#group by s.sales_first_name;

@app.route("/charts")
@login_required
def charts():
	activated = 6
	refused = 1
	no_answer = 4
	#probably want to use a dict for some of these values
	legend = 'Clients Activated'
	labels = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "December"]

	try:
		rep = current_user.username
		getonboarded = text('select s.sales_first_name, count(tic.id) from time t '
		+ 'join ticket tic '
		+ 'on t.cx_id = tic.account_id '
		+ 'join sales__rep s  '
		+ 'on s.sales_rep_id = t.assigned_by '
		+ 'where tic.o365status = "onboarded" '
		+ 'group by s.sales_first_name '			
		+ 'having s.sales_first_name = "{}";'.format(rep))
		sql = db.engine.execute(getonboarded)
		onboard_stats = sql.fetchall()
		#print (onboard_stats)

		getnotwant = ("select s.sales_first_name, count(tic.o365status) from time t "
			+ "join ticket tic "
			+ "on t.cx_id = tic.account_id "
			+ "join sales__rep s "
			+ "on s.sales_rep_id = t.assigned_by "
			+ "where tic.o365status = 'Does not want' "
			+ "group by s.sales_first_name "
			+ "having sales_first_name = '{}';".format(rep))
		sql1 = db.engine.execute(getnotwant)
		notwant_status = sql1.fetchall()
		#print (notwant_status)

		getnocontact = text("select s.sales_first_name, count(tic.o365status) from time t "
			+ "join ticket tic "
			+ "on t.cx_id = tic.account_id "
			+ "join sales__rep s "
			+ "on s.sales_rep_id = t.assigned_by "
			+ "where tic.o365status = 'No Contact' "
			+ "group by s.sales_first_name "
			+ "having sales_first_name = '{}';".format(rep))
		sql2 = db.engine.execute(getnocontact)
		nocontact_status = sql2.fetchall()
		#print (nocontact_status)

		getincorrect = text("select s.sales_first_name, count(tic.o365status) from time t "
			+ "join ticket tic "
			+ "on t.cx_id = tic.account_id "
			+ "join sales__rep s "
			+ "on s.sales_rep_id = t.assigned_by "
			+ "where tic.o365status = 'Incorrect contact number' "
			+ "group by s.sales_first_name "
			+ "having sales_first_name = '{}';".format(rep))
		sql3 = db.engine.execute(getincorrect)
		incorrect_status = sql3.fetchall()
		#print(total_status)

		gettotal = text("select s.sales_first_name, count(tic.o365status) from time t "
			+ "join ticket tic "
			+ "on t.cx_id = tic.account_id "
			+ "join sales__rep s "
			+ "on s.sales_rep_id = t.assigned_by "
			+ "group by s.sales_first_name "
			+ "having sales_first_name = '{}';".format(rep))
		sql4 = db.engine.execute(gettotal)
		total_status = sql4.fetchall()
		print(total_status)

	except:
	 	print("I wasn't able to query the reps stats")
	values = [10, 9, 8, 7, 6, 4, 7, 8]
	ac_label = "red"
	re_label = "yellow"
	no_label = "blue"
	return render_template('charts.html', total_status=total_status, incorrect_status=incorrect_status, onboard_stats=onboard_stats, nocontact_status=nocontact_status, notwant_status=notwant_status, values=values, labels=labels, legend=legend, activated=activated, refused=refused, no_answer=no_answer)