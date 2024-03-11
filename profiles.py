from flask import Blueprint, render_template

profile = Blueprint("profile", __name__, url_prefix="/profile")


@profile.route("/")
def index():
    return render_template("profile.html")
