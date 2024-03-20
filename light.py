from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    jsonify,
)
from db import mysql

light = Blueprint("light", __name__, url_prefix="/light")


@light.route("/")
def index():
    current_user_id = session.get("user_id")
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM light_devices WHERE user_id = %s", (current_user_id,))
    devices = cur.fetchall()
    return render_template("light.html", devices=devices)


@light.route("/add", methods=["POST"])
def add_device():
    if request.is_json:
        data = request.json
        room = data.get("room")
    else:
        room = request.form.get("room")
    current_user_id = session.get("user_id")
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO light_devices (user_id, room, setting) VALUES (%s, %s, %s)",
        (current_user_id, room, 0),
    )
    mysql.connection.commit()
    return jsonify({"message": "Light Device added successfully"}), 200


@light.route("/update", methods=["POST"])
def update_device():
    if request.is_json:
        data = request.json
        device_id = data.get("device_id")
        setting = data.get("setting")
    else:
        device_id = request.form.get("device_id")
        setting = request.form.get("setting")
    cur = mysql.connection.cursor()
    cur.execute(
        "UPDATE light_devices SET setting = %s WHERE id = %s", (setting, device_id)
    )
    mysql.connection.commit()
    return jsonify({"message": "Light device updated successfully"}), 200


@light.route("/delete", methods=["POST"])
def delete_device():
    if request.is_json:
        data = request.json
        device_id = data.get("device_id")
    else:
        device_id = request.form.get("device_id")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM light_devices WHERE id = %s", (device_id,))
    mysql.connection.commit()
    return jsonify({"message": "Light Device deleted successfully"}), 200
