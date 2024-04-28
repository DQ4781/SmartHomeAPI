from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
import re

auth = Blueprint("auth", __name__, url_prefix="/auth")

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/") # Assuming MongoDB is running locally on the default port
db = client.smart_home  # Accessing the "smart_home" database
users_collection = db.users  # Accessing the "users" collection

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Invalid email address.")
            return render_template("register.html"), 422

        # Check if username exists
        if users_collection.find_one({"username": username}):
            flash("Username already exists.")
            return render_template("register.html"), 409

        # Check if email exists
        if users_collection.find_one({"email": email}):
            flash("This email is in use.")
            return render_template("register.html"), 409

        # Insert user into the collection
        user_data = {"username": username, "password": password, "email": email}
        users_collection.insert_one(user_data)
        flash("Registration successful! Please log in.")
        return redirect(url_for("auth.login")), 200

    return render_template("register.html")

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Check if user exists with provided credentials
        account = users_collection.find_one({"username": username, "password": password})

        if account:
            # Convert ObjectId to string before storing in the session
            session["user_id"] = str(account["_id"])
            return redirect(url_for("home.index"))
        else:
            msg = "Incorrect username or password!"
            return render_template("login.html", msg=msg), 401
    return render_template("login.html")

@auth.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("auth.login"))

