from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, DataRequired, EqualTo, Email, ValidationError, session, flash
from db import mysql
from forms import *
import re

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]

        # Basic validation (you can expand this as needed)
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Invalid email address.")
            return render_template("register.html")

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        account = cur.fetchone()
        if account:
            flash("Username already exists.")
            return render_template("register.html")

        cur.execute(
            "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
            (username, password, email),
        )
        mysql.connection.commit()
        flash("Registration successful! Please log in.")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM users WHERE username = %s AND password = %s",
            (username, password),
        )
        account = cur.fetchone()
        if account:
            session["user_id"] = account[0]  # Store user ID in session
            return redirect(url_for("home.index"))
        else:
            msg = "Incorrect username or password!"
            return render_template("login.html", msg=msg)
    return render_template("login.html")


@auth.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("auth.login"))
@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        return redirect(url_for("auth.home"))
    if form.errors!={}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('register.html',form=form)
