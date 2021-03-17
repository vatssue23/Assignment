from flask import Blueprint
from flask import render_template


main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("home.html", title="HOME")


@main.route("/about")
def about():
    return render_template("about.html", title="ABOUT")
