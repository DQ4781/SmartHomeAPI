from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app import mysql

profile = Blueprint("profile", __name__, url_prefix="/profile")


@profile.route("/")
def index():
    current_user_id = session.get("user_id")
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (current_user_id,))
    user_details = cur.fetchone()
    return render_template("profile.html", user=user_details)
