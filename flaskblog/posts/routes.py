"""Application routes."""
from flask import render_template, flash, redirect, url_for, request, abort, Blueprint
from flask_login import current_user, login_required

from flaskblog.posts.forms import AddPostForm
from flaskblog.models import User, Post
from flaskblog import db

posts = Blueprint("posts", __name__)


@posts.route("/posts/add", methods=["GET", "POST"])
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
        return redirect(url_for("main.home"))
    return render_template("add_post.html", title="Add Post", form=form)


@posts.route("/posts/<int:post_id>")
@login_required
def get_post(post_id):
    """."""
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)


@posts.route("/posts/<int:post_id>/update", methods=["GET", "POST"])
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
            return redirect(url_for("posts.update_post", post_id=post.id))
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your post has been updated", category="success")
        return redirect(url_for("posts.get_post", post_id=post.id))
    form.title.data = post.title
    form.content.data = post.content
    return render_template("update_post.html", title=post.title, post=post, form=form)


@posts.route("/posts/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    """."""
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted", category="success")
    return redirect(url_for("main.home"))


@posts.route("/posts/<string:username>")
@login_required
def get_posts_by_username(username):
    """."""
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
                      .order_by(Post.created_at.desc())\
                      .paginate(page=page, per_page=5)
    return render_template("user_post.html", posts=posts, user=user)
