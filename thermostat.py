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

thermostat = Blueprint("thermostat", __name__, url_prefix="/thermostat")


@thermostat.route("/")
def index():
    # Fetch connected thermostat devices from the database
    current_user_id = session.get("user_id")
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT * FROM thermostat_devices WHERE user_id = %s", (current_user_id,)
    )
    devices = cur.fetchall()
    return render_template("thermostat.html", devices=devices)


@thermostat.route("/add", methods=["POST"])
def add_device():
    if request.is_json:
        data = request.json
        room = data.get("room")
    else:
        room = request.form.get("room")
    current_user_id = session.get("user_id")
    # Add the new device to the database
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO thermostat_devices (user_id, room, setting) VALUES (%s, %s, %s)",
        (current_user_id, room, 50),
    )
    mysql.connection.commit()
    return jsonify({"message": "Thermostat Device added successfully"}), 200


@thermostat.route("/update", methods=["POST"])
def update_device():
    if request.is_json:
        data = request.json
        device_id = data.get("device_id")
        setting = data.get("setting")
    else:
        device_id = request.form.get("device_id")
        setting = request.form.get("setting")
    # Update the device setting in the database
    cur = mysql.connection.cursor()
    cur.execute(
        "UPDATE thermostat_devices SET setting = %s WHERE id = %s", (setting, device_id)
    )
    mysql.connection.commit()
    return jsonify({"message": "Thermostat Device updated successfully"}), 200


@thermostat.route("/delete", methods=["POST"])
def delete_device():
    if request.is_json:
        data = request.json
        device_id = data.get("device_id")
    else:
        device_id = request.form.get("device_id")
    # Delete the device from the database
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM thermostat_devices WHERE id = %s", (device_id,))
    mysql.connection.commit()
    return jsonify({"message": "Thermostat Device deleted successfully"}), 200
