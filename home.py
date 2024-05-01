from flask import Blueprint, render_template
from jwt_token import token_required

home = Blueprint("home", __name__, url_prefix="/home")


@home.route("/", methods=["GET"])
@token_required
def index(current_user):
    return render_template("home.html")
