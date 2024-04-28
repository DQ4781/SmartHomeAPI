from flask import Flask, redirect, url_for
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

if __name__ == "__main__":
    app.run(debug=True, port=8081)
