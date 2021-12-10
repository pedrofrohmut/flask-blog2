"""Application routes."""
import secrets
import os

from PIL import Image
from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import login_user, current_user, logout_user, login_required

from flaskblog.forms import SignUpForm, SignInForm, UpdateAccountForm, AddPostForm
from flaskblog.models import User, Post
from flaskblog import app, db, bcrypt


@app.route("/")
@app.route("/home")
def home():
    """Home and Root Route."""
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.created_at.desc()).paginate(per_page=5, page=page)
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
                  + "Please retry or go to sign up if you are not yet registered",
                  category="error")
            return redirect(url_for("signin"))
        is_password_valid = bcrypt.check_password_hash(user.password_hash,
                                                       form.password.data)
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


def size_down_image(form_image):
    """Size down images using pillow."""
    output_size = (125, 125)
    new_image = Image.open(form_image)
    new_image.thumbnail(output_size)
    return new_image


def save_image(form_image):
    """Save image."""
    random_hex = secrets.token_hex(8)
    _, file_extension = os.path.splitext(form_image.filename)
    image_file_name = random_hex + file_extension
    image_path = os.path.join(app.root_path, "static/profile_pics", image_file_name)
    sized_down_image = size_down_image(form_image)
    sized_down_image.save(image_path)
    return image_file_name


@app.route("/account", methods=["GET", "POST"])
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
            return redirect(url_for("account"))
        if form.image.data:
            image_file = save_image(form.image.data)
            current_user.image_file = image_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated", category="success")
        return redirect(url_for("account"))
    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
    form.username.data = current_user.username
    form.email.data = current_user.email
    return render_template("account.html",
                           title="Account", image_file=image_file, form=form)


@app.route("/posts/add", methods=["GET", "POST"])
@login_required
def add_post():
    """Add a post form and adding to database."""
    form = AddPostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data,
                    user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash("Your post had been added", category="success")
        return redirect(url_for("home"))
    return render_template("add_post.html", title="Add Post", form=form)


@app.route("/posts/<int:post_id>")
@login_required
def get_post(post_id):
    """."""
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)


@app.route("/posts/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    """."""
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = AddPostForm()
    if form.validate_on_submit():
        same_title = form.title.data == post.title
        print("SAME TITLE =  ", same_title)
        same_content = form.content.data == post.content
        print("SAME CONTENT = ", same_content)
        if same_title and same_content:
            flash("There are no changes to be commited. Nothing changed",
                  category="info")
            return redirect(url_for("update_post", post_id=post.id))
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your post has been updated", category="success")
        return redirect(url_for("get_post", post_id=post.id))
    form.title.data = post.title
    form.content.data = post.content
    return render_template("update_post.html", title=post.title, post=post, form=form)


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    """."""
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted", category="success")
    return redirect(url_for("home"))


@app.route("/posts/<string:username>")
@login_required
def get_posts_by_username(username):
    """."""
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
                      .order_by(Post.created_at.desc())\
                      .paginate(page=page, per_page=5)
    return render_template("user_post.html", posts=posts, user=user)
