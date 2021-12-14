"""Database models."""
# Using __main__ instead of app to workaround python import cycling
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from flaskblog import db, login_manager, app


@login_manager.user_loader
def load_user(user_id):
    """Find user by id."""
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """User database model for sqlalchemy."""

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password_hash = db.Column(db.String(60), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    posts = db.relationship("Post", backref=db.backref("author", lazy=True))

    def get_reset_token(self, expires_in=1800):
        """."""
        serializer = Serializer(app.config["SECRET_KEY"], expires_in=expires_in)
        reset_token = serializer.dumps({"user_id": self.id}).decode("UTF-8")
        return reset_token

    @staticmethod
    def verify_reset_token(token):
        """."""
        serializer = Serializer(app.config["SECRET_KEY"])
        try:
            user_id = serializer.loads(token)["user_id"]
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        """Magic Method: Represent a user object as a string."""
        return f"User ('{self.username}', '{self.email}', {self.image_file})"


class Post(db.Model):
    """Post database model for sqlalchemy."""

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        """Magic method: Represent a post object as a string."""
        return f"Post ('{self.title}', '{self.created_at}')"
