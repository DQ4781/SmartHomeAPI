from flask import Blueprint, render_template, request, redirect, url_for, session
from app import mysql

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username]"]
        password = request.form["password"]
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM users WHERE username = %s AND password = %s",
            (username, password),
        )
        account = cur.fetchone()
        if account:
            session["user_id"] = account["id"]  # Store user ID in session
            return redirect(url_for("home.index"))
        else:
            msg = "Incorrect username or password!"
            return render_template("login.html", msg=msg)
    return render_template("login.html")


@auth.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("auth.login"))
