"""Users routes."""
from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required

from flaskblog.users.forms import (SignUpForm, SignInForm, UpdateAccountForm,
                                   RequestResetPasswordForm, ResetPasswordForm)
from flaskblog.models import User
from flaskblog.users.utils import save_image, send_password_reset_email
from flaskblog import db, bcrypt

users = Blueprint("users", __name__)


@users.route("/signup", methods=["GET", "POST"])
def signup():
    """Sign Up Route."""
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = SignUpForm()
    if form.validate_on_submit():
        password_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}. You can now sign in.", category="success")
        return redirect(url_for("main.home"))
    return render_template("signup.html", title="Sign Up", form=form)


@users.route("/signin", methods=["GET", "POST"])
def signin():
    """Sign In Route."""
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash(f"No user found with e-mail: {form.email.data}."
                  + "Please retry or go to sign up if you are not yet registered",
                  category="error")
            return redirect(url_for("users.signin"))
        is_password_valid = bcrypt.check_password_hash(user.password_hash,
                                                       form.password.data)
        if not is_password_valid:
            flash(f"The password is wrong or does not match e-mail: {form.email.data}."
                  + "Please recheck your password and e-mail", category="error")
            return redirect(url_for("users.signin"))
        login_user(user, remember=form.remember_me.data)
        flash(f"{form.email.data} successfully signed in", category="success")
        # Page to go next when login_required blocks a route
        next_param = request.args.get("next")
        if next_param:
            return redirect(next_param)
        return redirect(url_for("main.home"))
    return render_template("signin.html", title="Sign In", form=form)


@users.route("/signout")
def signout():
    """Sign out the current user."""
    logout_user()
    return redirect(url_for("main.home"))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    """Show current user account details."""
    form = UpdateAccountForm()
    if form.validate_on_submit():
        same_username = current_user.username == form.username.data
        same_email = current_user.email == form.email.data
        if same_username and same_email and not form.image.data:
            flash("There are no changes to be commited. Nothing changed",
                  category="info")
            return redirect(url_for("users.account"))
        if form.image.data:
            image_file = save_image(form.image.data)
            current_user.image_file = image_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated", category="success")
        return redirect(url_for("users.account"))
    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
    form.username.data = current_user.username
    form.email.data = current_user.email
    return render_template("account.html",
                           title="Account", image_file=image_file, form=form)


@users.route("/request_reset_password", methods=["GET", "POST"])
def request_reset_password():
    """."""
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RequestResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_password_reset_email(user)
        flash("An e-mail has been sent with instructions to reset your password", category="info")
        return redirect(url_for("users.signin"))
    return render_template("request_reset_password.html", form=form, title="Request Reset Password")


@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    """."""
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_token(token)
    if not user:
        flash("That token is expired or invalid", category="warning")
        return redirect(url_for("users.request_reset_password"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        password_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password_hash = password_hash
        db.session.commit()
        flash("Password has been updated. You can now sign in.", category="success")
        return redirect(url_for("users.signin"))
    return render_template("reset_password.html", title="Reset Password", form=form)
