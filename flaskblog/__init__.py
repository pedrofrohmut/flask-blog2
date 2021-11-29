"""App entry point."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = "f81f5a8bc4eaf45c1d7694833580abe3"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# Where to redirect when @login_required blocks access
login_manager.login_view = 'signin'
# Customize the flash message that show on blocking routes
login_manager.login_message = 'Please sign in to access this page'
login_manager.login_message_category = 'warning'

from flaskblog import routes
