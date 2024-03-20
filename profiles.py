from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    jsonify,
)
from db import mysql

profile = Blueprint("profile", __name__, url_prefix="/profile")


@profile.route("/")
def index():
    current_user_id = session.get("user_id")
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (current_user_id,))
    user_details = cur.fetchone()
    return render_template("profile.html", user=user_details)


@profile.route("/update", methods=["POST"])
def update():
    current_user_id = session.get("user_id")
    if request.is_json:
        data = request.json
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
    else:
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
    cur = mysql.connection.cursor()
    cur.execute(
        "UPDATE users SET username = %s, email = %s, password = %s WHERE id = %s",
        (username, email, password, current_user_id),
    )
    mysql.connection.commit()
    if request.is_json:
        return jsonify({"message": "Profile updated successfully"}), 200
    else:
        flash("Profile updated successfully!")
        return redirect(url_for("profile.index"))


@profile.route("/delete", methods=["POST"])
def delete():
    current_user_id = session.get("user_id")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id = %s", (current_user_id,))
    mysql.connection.commit()
    session.pop("user_id", None)
    if request.is_json:
        return jsonify({"message": "Account deleted successfully"})
    else:
        flash("Account deleted successfully!")
        return redirect(url_for("auth.login"))
