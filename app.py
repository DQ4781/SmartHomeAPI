from flask import Flask, redirect, url_for, render_template
from pymongo import MongoClient

app = Flask(__name__)

# Secret Key for Session Managment
app.secret_key = "thisisasecretkey"

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client.smart_home

from auth import auth
from home import home
from light import light
from thermostat import thermostat
from profiles import profile

app.register_blueprint(auth)
app.register_blueprint(home)
app.register_blueprint(light)
app.register_blueprint(thermostat)
app.register_blueprint(profile)


@app.route("/")
def index():
    return redirect(url_for("auth.login"))


@app.errorhandler(401)
def unauthorized(error):
    return render_template("401.html"), 401


@app.errorhandler(403)
def forbidden(error):
    return render_template("403.html"), 403


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(debug=True, port=8081)
