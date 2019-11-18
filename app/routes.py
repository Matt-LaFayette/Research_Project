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
				flash("success")
				if (user.role == "support"):
					return redirect(url_for('createticket'))
				if (user.role == "sales"):
					return redirect(url_for('searchcustomer'))
				

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
	month = int(now.month)
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
	return render_template('template.html', month=month, user=user, cx_info=cx_info, test=str(test))

#TEST
@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		username = form.username.data
		email=form.email.data
		role=form.userrole.data
		user = User(username=form.username.data, email=form.email.data, role=form.userrole.data)
		user.set_password(form.password.data)
		sql = text('INSERT INTO user (username, email, password_hash, role) VALUES ("{}", "{}", "{}", "{}");'.format(username, email, user.password_hash, role))
		db.engine.execute(sql)
		db.session.commit()
		# db.session.add(user)
		# db.session.commit()
		flash('Congratulations, you are now a registered user!')
		return redirect(url_for('index'))
	return render_template('register.html', title='Register', form=form)
#END TEST

@app.route('/salesorder', methods=('GET', 'POST'))
@login_required
def salesorder():
	form = Invoice()
	title = 'New Order'
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
	try:
		form = CreateCustomer()
		print("getting")
		customer = Customer(customer_fname=form.customer_fname.data, customer_lname=form.customer_lname.data, company_name=form.company_name.data, city=form.city.data, state=form.state.data, address=form.address.data, zip_code=form.zip_code.data, email=form.email.data, phone_num=form.phone_num.data)
		print("adding")
		db.session.add(customer)
		print("commiting")
		db.session.commit()
	except:
		db.session.rollback()
		print('I failed to create customer and rolled back')
	form = CreateCustomer()
	user = User.query.filter_by(username=current_user.username)
	title = 'Customer'
	return render_template('createcustomer.html', month=month, user=user, title=title, form=form)

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
			title = 'Tickets'
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
	return render_template('searchcustomer.html', month=month, user=user, title=title, form1=form1)

#this route is linked to searchcustomer and displays the results found
@app.route('/findaccount', methods=('GET', 'POST'))
@login_required
def findaccount():
	title = "Find Account"
	form = SearchCustomer()
	customerid = form.cx_id.data
	customerfname = form.customer_fname.data
	customerlname = form.customer_lname.data
	customer_phone_num = form.phone_num.data
	cxbyfname = ""
	cxbylname = ""
	cxbyphonenum = ""
	cxbyid = ""
	#Need to input logic so if someone enters name, then it then does a query to pull up the id by their name
	user = User.query.filter_by(username=current_user.username)
	if customerid:
		print("found customer id")
		cxbyid = Customer.query.filter_by(cx_id=customerid)
	if customerfname:
		print("found first name")
		cxbyfname = Customer.query.filter_by(customer_fname=customerfname)
	if customerlname:
		print("found last name")
		cxbylname = Customer.query.filter_by(customer_lname=customerlname)
	if customer_phone_num:
		print(customer_phone_num)
		cxbyphonenum = Customer.query.filter_by(phone_num=customer_phone_num)
		for x in cxbyphonenum:
			print(x)
	if form.validate_on_submit():
		x = 1
		for customer in cx:
			select = str(x) + 'Select'
			st = str(select)
			# selection = request.form.get(st)
			# print (selection)
			x = x + 1
			# session['name'] = customer.customer_name
	return render_template('findaccount.html', user=user, cxbyphonenum=cxbyphonenum, cxbyfname=cxbyfname, cxbylname=cxbylname, cxbyid=cxbyid, title=title)



@app.route('/test', methods=('GET', 'POST'))
def test():
	form = CreateCustomer()
	customer = Customer(customer_fname=form.customer_fname.data, customer_lname=form.customer_lname.data, company_name=form.company_name.data, city=form.city.data, state=form.state.data, address=form.address.data, zip_code=form.zip_code.data, email=form.email.data, phone_num=form.phone_num.data)
	try:
		db.session.add(customer)
		db.session.commit()
	except IntegrityError:
		db.session.rollback()
		return 'I failed and rolled back'
	# x = request.form['temptest']
	cx = Customer.query.filter_by(customer_fname=form.customer_fname.data, customer_lname=form.customer_lname.data, company_name=form.company_name.data, city=form.city.data, state=form.state.data, address=form.address.data, zip_code=form.zip_code.data, email=form.email.data, phone_num=form.phone_num.data).all()
	# session['response']= x
	# for x in cx:
	# 	print(x.cx_id)
	title = "Add"
	user = User.query.filter_by(username=current_user.username)
	return render_template('test.html', user=user, title=title, test=test, customer=cx)

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
			session['hour'] = str(x.hour)
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
		print("day: " + request.form['inputGroupSelect03'])
		day = request.form['inputGroupSelect03']
		print("time: " + request.form['inputGroupSelect06'])
		appt_time = request.form['inputGroupSelect06']
		sql_get_id = text("SELECT sales_rep_id from sales__rep WHERE sales_first_name= '{}';".format(current_user.username))
		sql_id = db.engine.execute(sql_get_id)
		assigned_by = sql_id.fetchone()
		print("assigned: " + str(assigned_by[0]))
		apptime = Time(month=month, day=day, hour=appt_time, cx_id=session['id'], assigned_by=assigned_by[0])
		db.session.add(apptime)
		db.session.commit()
		print("Successfully added appt to db")
	except:
	 	print("month and or time failed")
	try:
		sqlquery = text("SELECT month, day, date_format(hour, '%l%p') from time;")
		sql = db.engine.execute(sqlquery)
		testtime = sql.fetchall()
	except:
		print("unable to query time")
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
	daysinmonth = monthrange(2019,10)[1]
	title="Calendar"
	return render_template('calendar.html', title=title, daysinmonth=daysinmonth, form=form, month=month, user=user, cal=cal, testtime=testtime)

@app.route("/getdays/<month>", methods=('GET', 'POST'))
def getdays(month):
	daysinmonth = monthrange(2019,10)
	return str(daysinmonth)

#route for line graph
# @app.route("/simple_chart")
# @login_required
# def chart():
# 	legend = 'Clients Activated'
# 	labels = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "December"]
# 	values = [10, 9, 8, 7, 6, 4, 7, 8]
# 	return render_template('chart.html', values=values, labels=labels, legend=legend)

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
		# print(total_status)

	except:
	 	print("I wasn't able to query the reps stats")

	x=1
	total_month_stats = []
	values = []

	# numbers do not look correct?
	if (current_user.role != 'manager'):
		for x in range(1,13):
			getmonthtotal = text("select count(t.month), s.sales_first_name from time t " +
			"join sales__rep s " +
			"on s.sales_rep_id = t.assigned_by " +
			"join ticket tic " +
			"on tic.account_id = t.cx_id "
			"where t.month = '{}' and tic.o365status = 'onboarded' and s.sales_first_name = '{}' ".format(x,rep) +
			"group by s.sales_first_name;")
			sqlmonth = db.engine.execute(getmonthtotal)
			test = sqlmonth.fetchall()
			total_month_stats.append(test)
			if total_month_stats[x-1]:
				values.append(total_month_stats[x-1][0][0])
			else:
				values.append(0)
			x = x + 1
	elif (current_user.role == 'manager'):
		for x in range(1,13):
			getmonthtotal = text("select count(t.month)from time t " +
			"join sales__rep s " +
			"on s.sales_rep_id = t.assigned_by " +
			"join ticket tic " +
			"on tic.account_id = t.cx_id "
			"where t.month = '{}' and tic.o365status = 'onboarded';".format(x))
			sqlmonth = db.engine.execute(getmonthtotal)
			test = sqlmonth.fetchall()
			total_month_stats.append(test)
			if total_month_stats[x-1]:
				values.append(total_month_stats[x-1][0][0])
			else:
				values.append(0)
			x = x + 1
	#gets individual month value
	#print(total_month_stats[2][0][0])
	#out of range
	#print(total_month_stats[0][0])
	
	# manager only parts
	#maybe have it when a manager clicks on a name it goes to new route that takes name as param

	#list of all sales reps
	getsalesreps = text('select sales_first_name, sales_last_name from sales__rep;')
	sqlgetsalesreps = db.engine.execute(getsalesreps)
	sales_rep_list = sqlgetsalesreps.fetchall()
	# print (sales_rep_list)
	sales_rep_arry = []
	sales_rep_arry_fail = []
	outer_sales_rep_array = []
	for x in sales_rep_list:
		rep = x[0]
		getonboardedforemp = text('select s.sales_first_name, count(tic.id) from time t '
		+ 'join ticket tic '
		+ 'on t.cx_id = tic.account_id '
		+ 'join sales__rep s  '
		+ 'on s.sales_rep_id = t.assigned_by '
		+ 'where tic.o365status = "onboarded" '
		+ 'group by s.sales_first_name '			
		+ 'having s.sales_first_name = "{}";'.format(rep))
		sql = db.engine.execute(getonboardedforemp)
		emp_onboard_stats = sql.fetchall()
		sales_rep_arry.append(emp_onboard_stats)

		getnoactivateforemp = text('select s.sales_first_name, count(tic.id) from time t '
		+ 'join ticket tic '
		+ 'on t.cx_id = tic.account_id '
		+ 'join sales__rep s  '
		+ 'on s.sales_rep_id = t.assigned_by '
		+ 'where tic.o365status != "onboarded" '
		+ 'group by s.sales_first_name '			
		+ 'having s.sales_first_name = "{}";'.format(rep))
		sql2 = db.engine.execute(getnoactivateforemp)
		emp_noactivate_stats = sql2.fetchall()
		sales_rep_arry_fail.append(emp_noactivate_stats)
		#outer_sales_rep_array.append(sales_rep_arry)

	#gets total onboarded clients for the team
	totalonboarded = text('select s.sales_first_name, count(tic.id) from time t '
	+ 'join ticket tic '
	+ 'on t.cx_id = tic.account_id '
	+ 'join sales__rep s  '
	+ 'on s.sales_rep_id = t.assigned_by '
	+ 'where tic.o365status = "onboarded" '
	+ 'group by s.sales_first_name;')
	sql = db.engine.execute(totalonboarded)
	total_onboard_stats = sql.fetchall()
	total_all_onboard = 0
	for x in total_onboard_stats:
		total_all_onboard = total_all_onboard + x[1]

	#gets total clients that refused for the team
	totalnotwant = text('select s.sales_first_name, count(tic.id) from time t '
	+ 'join ticket tic '
	+ 'on t.cx_id = tic.account_id '
	+ 'join sales__rep s  '
	+ 'on s.sales_rep_id = t.assigned_by '
	+ 'where tic.o365status = "Does not want" '
	+ 'group by s.sales_first_name;')
	sql = db.engine.execute(totalnotwant)
	total_notwant_stats = sql.fetchall()
	total_all_notwant = 0
	for x in total_notwant_stats:
		total_all_notwant = total_all_notwant + x[1]


	#gets total clients that support was unable to contact (for the team)
	totalnocontact = text('select s.sales_first_name, count(tic.id) from time t '
	+ 'join ticket tic '
	+ 'on t.cx_id = tic.account_id '
	+ 'join sales__rep s  '
	+ 'on s.sales_rep_id = t.assigned_by '
	+ 'where tic.o365status = "No Contact" '
	+ 'group by s.sales_first_name;')
	sql = db.engine.execute(totalnocontact)
	total_nocontact_stats = sql.fetchall()
	total_all_nocontact = 0
	for x in total_nocontact_stats:
		total_all_nocontact = total_all_nocontact + x[1]

	#gets total clients that had incorrect contact info for the team
	totalincorrectcontact = text('select s.sales_first_name, count(tic.id) from time t '
	+ 'join ticket tic '
	+ 'on t.cx_id = tic.account_id '
	+ 'join sales__rep s  '
	+ 'on s.sales_rep_id = t.assigned_by '
	+ 'where tic.o365status = "Incorrect contact number" '
	+ 'group by s.sales_first_name;')
	sql = db.engine.execute(totalincorrectcontact)
	total_incorrectcontact_stats = sql.fetchall()
	total_all_incorrectcontact = 0
	for x in total_incorrectcontact_stats:
		total_all_incorrectcontact = total_all_incorrectcontact + x[1]

	legend = 'Clients Activated'
	labels = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
	ac_label = "red"
	re_label = "yellow"
	no_label = "blue"
	if (current_user.role != "manager"):
		return render_template('charts.html', total_status=total_status, incorrect_status=incorrect_status, onboard_stats=onboard_stats, nocontact_status=nocontact_status, notwant_status=notwant_status, values=values, labels=labels, legend=legend)
	return render_template('managercharts.html', values=values, labels=labels, legend=legend, sales_rep_arry_fail=sales_rep_arry_fail, zip=zip, sales_rep_arry=sales_rep_arry, total_all_onboard=total_all_onboard, total_all_notwant=total_all_notwant, total_all_nocontact=total_all_nocontact, total_all_incorrectcontact=total_all_incorrectcontact)

@app.route("/teamstats/<rep>")
@login_required
def teamstats(rep):
	sr = rep
	try:
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
		if (not onboard_stats):
			onboard_stats.append((rep, 0))
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
		if (not notwant_status):
			notwant_status.append((rep, 0))
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
		if (not nocontact_status):
			nocontact_status.append((rep, 0))
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
		if (not incorrect_status):
			incorrect_status.append((rep, 0))
		#print(incorrect_status)

		gettotal = text("select s.sales_first_name, count(tic.o365status) from time t "
			+ "join ticket tic "
			+ "on t.cx_id = tic.account_id "
			+ "join sales__rep s "
			+ "on s.sales_rep_id = t.assigned_by "
			+ "group by s.sales_first_name "
			+ "having sales_first_name = '{}';".format(rep))
		sql4 = db.engine.execute(gettotal)
		total_status = sql4.fetchall()
		if (not total_status):
			total_status.append((rep, 0))
		#print(total_status)
	except:
		print("team stats failed")
	total_month_stats = []
	values = []
	for x in range(1,13):
		getmonthtotal = text("select count(t.month), s.sales_first_name from time t " +
		"join sales__rep s " +
		"on s.sales_rep_id = t.assigned_by " +
		"join ticket tic " +
		"on tic.account_id = t.cx_id "
		"where t.month = '{}' and tic.o365status = 'onboarded' and s.sales_first_name = '{}' ".format(x,rep) +
		"group by s.sales_first_name;")
		sqlmonth = db.engine.execute(getmonthtotal)
		test = sqlmonth.fetchall()
		total_month_stats.append(test)
		if total_month_stats[x-1]:
			#print(x)
			values.append(total_month_stats[x-1][0][0])
		else:
			values.append(0)
		x = x + 1
	legend = 'Clients Activated'
	labels = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
	ac_label = "red"
	re_label = "yellow"
	no_label = "blue"
	return render_template('teamstats.html', values=values, labels=labels, total_status=total_status, incorrect_status=incorrect_status, nocontact_status=nocontact_status, notwant_status=notwant_status, onboard_stats=onboard_stats, sr=sr)

#probably will need to pass in rep name to url
@app.route("/Activated/<rep>")
@login_required
def Activated(rep):
	if (rep != "All"):
		onboarded_details= text('select s.sales_first_name, tic.o365status, tic.id, tic.description, tic.account_id, tic.assigned_to, tic.contact_name, s.sales_rep_id, s.sales_first_name from time t ' +
		'join ticket tic ' +
		'on t.cx_id = tic.account_id ' +
		'join sales__rep s ' + 
		'on s.sales_rep_id = t.assigned_by ' +
		'where tic.o365status = "onboarded" and s.sales_first_name = "{}";'.format(rep))
		sql5 = db.engine.execute(onboarded_details)
		onboarded_query_details = sql5.fetchall()

	elif (rep == "All"):
		onboarded_details= text('select s.sales_first_name, tic.o365status, tic.id, tic.description, tic.account_id, tic.assigned_to, tic.contact_name, s.sales_rep_id, s.sales_first_name from time t ' +
		'join ticket tic ' +
		'on t.cx_id = tic.account_id ' +
		'join sales__rep s ' + 
		'on s.sales_rep_id = t.assigned_by ' +
		'where tic.o365status = "onboarded" ' +
		'order by s.sales_rep_id;')
		sql5 = db.engine.execute(onboarded_details)
		onboarded_query_details = sql5.fetchall()

	return render_template('Activated.html', onboarded_query_details=onboarded_query_details)

@app.route("/Incorrect_Contact/<rep>")
@login_required
def Incorrect_Contact(rep):
	if (rep != "All"):
		Incorrect_details= text('select s.sales_first_name, tic.o365status, tic.id, tic.description, tic.account_id, tic.assigned_to, tic.contact_name, s.sales_rep_id, s.sales_first_name from time t ' +
		'join ticket tic ' +
		'on t.cx_id = tic.account_id ' +
		'join sales__rep s ' + 
		'on s.sales_rep_id = t.assigned_by ' +
		'where tic.o365status = "Incorrect contact number" and s.sales_first_name = "{}";'.format(rep))
		sql6 = db.engine.execute(Incorrect_details)
		Incorrect_query_details = sql6.fetchall()

	elif (rep == "All"):
		Incorrect_details= text('select s.sales_first_name, tic.o365status, tic.id, tic.description, tic.account_id, tic.assigned_to, tic.contact_name, s.sales_rep_id, s.sales_first_name from time t ' +
		'join ticket tic ' +
		'on t.cx_id = tic.account_id ' +
		'join sales__rep s ' + 
		'on s.sales_rep_id = t.assigned_by ' +
		'where tic.o365status = "Incorrect contact number" ' +
		'order by s.sales_rep_id;')
		sql6 = db.engine.execute(Incorrect_details)
		Incorrect_query_details = sql6.fetchall()

	return render_template('Incorrect_Contact.html', Incorrect_query_details=Incorrect_query_details)


@app.route("/Refused/<rep>")
@login_required
def Refused(rep):
	if (rep != "All"):
		refused_details= text('select s.sales_first_name, tic.o365status, tic.id, tic.description, tic.account_id, tic.assigned_to, tic.contact_name, s.sales_rep_id, s.sales_first_name from time t ' +
		'join ticket tic ' +
		'on t.cx_id = tic.account_id ' +
		'join sales__rep s ' + 
		'on s.sales_rep_id = t.assigned_by ' +
		'where tic.o365status = "Does not want" and s.sales_first_name = "{}";'.format(rep))
		sql7 = db.engine.execute(refused_details)
		refused_query_details = sql7.fetchall()

	elif (rep == "All"):
		refused_details= text('select s.sales_first_name, tic.o365status, tic.id, tic.description, tic.account_id, tic.assigned_to, tic.contact_name, s.sales_rep_id, s.sales_first_name from time t ' +
		'join ticket tic ' +
		'on t.cx_id = tic.account_id ' +
		'join sales__rep s ' + 
		'on s.sales_rep_id = t.assigned_by ' +
		'where tic.o365status = "Does not want" ' +
		'order by s.sales_rep_id;')
		sql7 = db.engine.execute(refused_details)
		refused_query_details = sql7.fetchall()

	return render_template('Refused.html', refused_query_details=refused_query_details)


@app.route("/No_Contact/<rep>")
@login_required
def No_Contact(rep):
	if (rep != "All"):
		contact_details= text('select s.sales_first_name, tic.o365status, tic.id, tic.description, tic.account_id, tic.assigned_to, tic.contact_name, s.sales_rep_id, s.sales_first_name from time t ' +
		'join ticket tic ' +
		'on t.cx_id = tic.account_id ' +
		'join sales__rep s ' + 
		'on s.sales_rep_id = t.assigned_by ' +
		'where tic.o365status = "No Contact" and s.sales_first_name = "{}";'.format(rep))
		sql8 = db.engine.execute(contact_details)
		contact_query_details = sql8.fetchall()

	elif (rep == "All"):
		contact_details= text('select s.sales_first_name, tic.o365status, tic.id, tic.description, tic.account_id, tic.assigned_to, tic.contact_name, s.sales_rep_id, s.sales_first_name from time t ' +
		'join ticket tic ' +
		'on t.cx_id = tic.account_id ' +
		'join sales__rep s ' + 
		'on s.sales_rep_id = t.assigned_by ' +
		'where tic.o365status = "No Contact" ' +
		'order by s.sales_rep_id;')
		sql8 = db.engine.execute(contact_details)
		contact_query_details = sql8.fetchall()

	return render_template('No_Contact.html', contact_query_details=contact_query_details)