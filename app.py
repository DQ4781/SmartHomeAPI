from flask import Flask, redirect, url_for
from flask_mysqldb import MySQL


app = Flask(__name__)


# DB CONNECTION STUFF: TODO AT A LATER TIME

app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "pass"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_DB"] = "smart_home"

mysql = MySQL(app)


import auth
import home
import light
import thermostat
import profiles


app.register_blueprint(auth.auth)
app.register_blueprint(home.home)
app.register_blueprint(light.light)
app.register_blueprint(thermostat.thermostat)
app.register_blueprint(profiles.profile)


@app.route("/")
def index():
    return redirect(url_for("auth.register"))


if __name__ == "__main__":
    app.run(debug=True)
