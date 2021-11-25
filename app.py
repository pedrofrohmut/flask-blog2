"""App entry point."""
from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from forms import SignUpForm, SignInForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "f81f5a8bc4eaf45c1d7694833580abe3"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
db = SQLAlchemy(app)

posts = [
    {
        "author": "Corey Schafer",
        "title": "Blog post 1",
        "content": "First post content",
        "created_at": "April 20, 2018"
    },
    {
        "author": "Jane Doe",
        "title": "Blog post 2",
        "content": "Second post content",
        "created_at": "April 21, 2019"
    }
]


class User(db.Model):
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


@app.route("/")
@app.route("/home")
def home():
    """Home and Root Route."""
    return render_template("home.html", posts=posts)


@app.route("/about")
def about():
    """About Route."""
    return render_template("about.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Sign Up Route."""
    form = SignUpForm()
    if form.validate_on_submit():
        flash(f"Account created for  {form.username.data}!", category="success")
        return redirect(url_for("home"))
    return render_template("signup.html", title="Sign Up", form=form)


@app.route("/signin", methods=["GET", "POST"])
def signin():
    """Sign In Route."""
    form = SignInForm()
    if form.validate_on_submit():
        flash(f"{form.email.data} successfully signed in", category="success")
        return redirect(url_for("home"))
    return render_template("signin.html", title="Sign In", form=form)


if __name__ == "__main__":
    app.run(debug=True)
