"""Application routes."""
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user, logout_user, login_required

from flaskblog.forms import SignUpForm, SignInForm
from flaskblog.models import User
from flaskblog import app, db, bcrypt

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
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = SignUpForm()
    if form.validate_on_submit():
        password_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}. You can now sign in.", category="success")
        return redirect(url_for("home"))
    return render_template("signup.html", title="Sign Up", form=form)


@app.route("/signin", methods=["GET", "POST"])
def signin():
    """Sign In Route."""
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash(f"No user found with e-mail: {form.email.data}."
                  + "Please retry or go to sign up if you are not yet registered", category="error")
            return redirect(url_for("signin"))
        is_password_valid = bcrypt.check_password_hash(user.password_hash, form.password.data)
        if not is_password_valid:
            flash(f"The password is wrong or does not match e-mail: {form.email.data}."
                  + "Please recheck your password and e-mail", category="error")
            return redirect(url_for("signin"))
        login_user(user, remember=form.remember_me.data)
        flash(f"{form.email.data} successfully signed in", category="success")
        # Page to go next when login_required blocks a route
        next_param = request.args.get("next")
        if next_param:
            return redirect(next_param)
        return redirect(url_for("home"))
    return render_template("signin.html", title="Sign In", form=form)


@app.route("/signout")
def signout():
    """Sign out the current user."""
    logout_user()
    return redirect(url_for("home"))


@app.route("/account")
@login_required
def account():
    """Show current user account details."""
    return render_template("account.html", title="Account")
