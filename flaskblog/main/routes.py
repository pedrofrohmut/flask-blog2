"""Main routes."""
from flask import Blueprint, request, render_template

from flaskblog.models import Post

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
def home():
    """Home and Root Route."""
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.created_at.desc()).paginate(per_page=5, page=page)
    return render_template("home.html", posts=posts)


@main.route("/about")
def about():
    """About Route."""
    return render_template("about.html")
