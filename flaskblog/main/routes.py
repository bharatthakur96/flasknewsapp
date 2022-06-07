from flask import render_template, request, Blueprint
from flaskblog.models import Post
from flaskblog.main.forms import SearchForm
from flaskblog.posts.routes import post


main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("home.html", posts=posts)


@main.route("/about")
def about():
    return render_template("about.html", title="About")


@main.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


@main.route("/search_post", methods=["POST"])
def search_post():
    # breakpoint()
    form = SearchForm()
    posts = Post.query
    if form.validate_on_submit():
        searched = form.searched.data
        posts = posts.filter(Post.content.like("%" + searched + "%"))
        posts = posts.order_by(Post.title).all()
        return render_template(
            "search_post.html", form=form, searched=searched, posts=posts
        )

