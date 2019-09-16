from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://matt:Elements1@localhost/crm_system'
app.debug = True
db = SQLAlchemy(app)
login = LoginManager(app)
migrate = Migrate(app, db)








#Secrete key for WTF forms
WTF_CSRF_SECRET_KEY = 'a random string'
SECRET_KEY = "test"
app.config['SECRET_KEY'] = SECRET_KEY

from app import routes, models