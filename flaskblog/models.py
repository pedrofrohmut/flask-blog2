"""Database models."""
# Using __main__ instead of app to workaround python import cycling
from datetime import datetime
from flask_login import UserMixin

from flaskblog import db, login_manager


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
