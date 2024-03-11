from flask import Blueprint, render_template, request, redirect, url_for
from app import mysql

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/login", methods=["GET", "POST"])
def login():
    # Login logic here
    return render_template("login.html")


@auth.route("/register", methods=["GET", "POST"])
def register():
    # Registration logic here
    return render_template("register.html")
