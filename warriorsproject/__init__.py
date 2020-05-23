import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from werkzeug.utils import secure_filename

login_manager = LoginManager()

app = Flask(__name__)

app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_DEFAULT_SENDER'] = "wareliteracing@gmail.com"
app.config['MAIL_USERNAME'] = "wareliteracing@gmail.com"
app.config['MAIL_PASSWORD'] = "Zapata99!"
mail = Mail(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = "mysecretkey"
app.config['TESTING'] = False
app.config['LOGIN_DISABLED'] = False
app.config['UPLOAD_FOLDER'] = basedir
### SQL DB Section #####

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

Migrate(app,db) # so you can make changes to actual db
# steps to migrate are - flask db migrate -m "something" then flask db upgrade

### login section
login_manager.init_app(app)
login_manager.login_view = 'login'

from warriorsproject.runners.views import runners_blueprint
from warriorsproject.coaches.views import coaches_blueprint

app.register_blueprint(coaches_blueprint, url_prefix='/coaches')
app.register_blueprint(runners_blueprint, url_prefix='/runners')
 