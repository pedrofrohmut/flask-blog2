"""App entry point."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from dotenv import load_dotenv

from flaskblog.config import Config

load_dotenv()

db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
login_manager = LoginManager()

# Where to redirect when @login_required blocks access
login_manager.login_view = 'users.signin'
# Customize the flash message that show on blocking routes
login_manager.login_message = 'Please sign in to access this page'
login_manager.login_message_category = 'warning'


def create_app(config_class=Config):
    """."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)

    return app
