from flask import Blueprint, render_template

thermostat = Blueprint("thermostat", __name__, url_prefix="/thermostat")


@thermostat.route("/")
def index():
    return render_template("thermostat.html")
