from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    jsonify,
    abort
)
from pymongo import MongoClient
from bson import ObjectId
import logging 

thermostat = Blueprint("thermostat", __name__, url_prefix="/thermostat")

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client.smart_home 

@thermostat.route("/")
def index():
    current_user_id = session.get("user_id")
    # Query MongoDB for thermostat devices
    devices = list(db.thermostat_devices.find({"user_id": current_user_id}))
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
    db.thermostat_devices.insert_one(
        {"user_id": current_user_id, "room": room, "setting": 50}
    )
    if request.is_json:
        return jsonify({"message": "Thermostat Device added successfully"}), 200
    else:
        return redirect(url_for("thermostat.index"))

@thermostat.route("/update", methods=["POST"])
def update_device():
    if request.is_json:
        data = request.json
        device_id = data.get("device_id")
        setting = data.get("setting")
    else:
        device_id = request.form.get("device_id")
        setting = request.form.get("setting")

    # Convert device_id to ObjectId
    device_id = ObjectId(device_id)
    # Update thermostat device in MongoDB
    db.thermostat_devices.update_one({"_id": device_id}, {"$set": {"setting": setting}})
    if request.is_json:
        return jsonify({"message": "Thermostat device updated successfully"}), 200
    else:
        return redirect(url_for("thermostat.index"))
    
@thermostat.route("/delete", methods=["POST"])
def delete_device():
    if request.is_json:
        data = request.json
        device_id = data.get("device_id")
    else:
        device_id = request.form.get("device_id")
    # Convert device_id to ObjectId
    device_id = ObjectId(device_id)
    # Delete light device from MongoDB
    db.thermostat_devices.delete_one({"_id": device_id})
    if request.is_json:
        return jsonify({"message": "Thermostat Device deleted successfully"}), 200
    else:
        return redirect(url_for("thermostat.index"))
