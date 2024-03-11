from flask import Blueprint, render_template

light = Blueprint("light", __name__, url_prefix="/light")


@light.route("/")
def index():
    return render_template("light.html")
