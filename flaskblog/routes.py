"""Application routes."""
from flask import render_template, flash, redirect, url_for

from flaskblog.forms import SignUpForm, SignInForm
from flaskblog.models import User, Post
from flaskblog import app

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
