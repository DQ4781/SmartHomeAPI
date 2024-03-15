from flask import Flask, redirect, url_for
from db import mysql


app = Flask(__name__)


# Secret Key for Session Managment
app.secret_key = "thisisasecretkey"

# MySQL configs
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_DB"] = "smart_home"
app.config["MYSQL_UNIX_SOCKET"] = "/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock"

mysql.init_app(app)


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
