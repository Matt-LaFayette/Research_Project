from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from flask_migrate import Migrate


app = Flask(__name__)
if __name__ == "__main__":
	app.run()
app.config.from_object(Config)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://matt:Elements1@localhost/crm_system'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://bcfb3fc3b457ff:fe8d2e38@us-cdbr-iron-east-02.cleardb.net/heroku_9302677d1154b2e?'
app.debug = True
db = SQLAlchemy(app)
login = LoginManager(app)
migrate = Migrate(app, db)








#Secrete key for WTF forms
WTF_CSRF_SECRET_KEY = 'a random string'
SECRET_KEY = "test"
app.config['SECRET_KEY'] = SECRET_KEY

from app import routes, models