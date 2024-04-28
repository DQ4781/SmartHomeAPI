from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    jsonify,
    flash
)
import os
from pymongo import MongoClient
from bson import ObjectId  # Import ObjectId

light = Blueprint("light", __name__, url_prefix="/light")

UPLOAD_FOLDER = os.path.abspath("uploads")
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client.smart_home  # Use your database name

@light.route("/")
def index():
    current_user_id = session.get("user_id")
    # Query MongoDB for light devices
    devices = db.light_devices.find({"user_id": current_user_id})
    
    device_dicts = []
    for device in devices:
        # Query MongoDB for device files
        files = db.device_files.find({"device_id": device["_id"]})
        device_dict = {
            "id": device["_id"],
            "user_id": device["user_id"],
            "room": device["room"],
            "setting": device["setting"],
            "files": [file["filename"] for file in files]
        }
        device_dicts.append(device_dict)
        
    return render_template("light.html", devices=device_dicts)


@light.route("/add", methods=["POST"])
def add_device():
    if request.is_json:
        data = request.json
        room = data.get("room")
    else:
        room = request.form.get("room")
    current_user_id = session.get("user_id")
    # Insert new light device into MongoDB
    db.light_devices.insert_one({"user_id": current_user_id, "room": room, "setting": 0})
    if request.is_json:
        return jsonify({"message": "Light Device added successfully"}), 200
    else:
        return redirect(url_for("light.index"))


@light.route("/update", methods=["POST"])
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
    # Update light device in MongoDB
    db.light_devices.update_one({"_id": device_id}, {"$set": {"setting": setting}})
    if request.is_json:
        return jsonify({"message": "Light device updated successfully"}), 200
    else:
        return redirect(url_for("light.index"))

@light.route("/delete", methods=["POST"])
def delete_device():
    if request.is_json:
        data = request.json
        device_id = data.get("device_id")
    else:
        device_id = request.form.get("device_id")
    # Convert device_id to ObjectId
    device_id = ObjectId(device_id)
    # Delete light device from MongoDB
    db.light_devices.delete_one({"_id": device_id})
    if request.is_json:
        return jsonify({"message": "Light Device deleted successfully"}), 200
    else:
        return redirect(url_for("light.index"))


@light.route("/upload", methods=["POST"])
def upload_file():
    device_id = request.form.get("device_id")
    file = request.files["file"]
    if file:
        # Save the file to the server
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        # Save file information to MongoDB
        db.device_files.insert_one({"device_id": ObjectId(device_id), "filename": file.filename})
        flash("File uploaded successfully")
    return redirect(url_for("light.index"))


@light.route("/remove", methods=["POST"])
def remove_file():
    device_id = request.form.get("device_id")
    file_to_remove = request.form.get("file_to_remove")
    # Remove file from the server
    file_path = os.path.join(UPLOAD_FOLDER, file_to_remove)
    if os.path.exists(file_path):
        os.remove(file_path)
        # Remove file information from MongoDB
        db.device_files.delete_one({"device_id": ObjectId(device_id), "filename": file_to_remove})
        flash("File removed successfully")
    return redirect(url_for("light.index"))

