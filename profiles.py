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
from pymongo import MongoClient
from bson import ObjectId

profile = Blueprint("profile", __name__, url_prefix="/profile")

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client.smart_home

@profile.route("/")
def index():
    current_user_id = session.get("user_id")
    # Convert current_user_id to ObjectId
    user_id_object = ObjectId(current_user_id)
    # Query MongoDB for user details
    user_details = db.users.find_one({"_id": user_id_object})
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

    user_id_object = ObjectId(current_user_id)
    # Remove password update if not provided
    update_data = {"username": username, "email": email}
    if password:
        update_data["password"] = password

    try:
        # Update user details in MongoDB
        result = db.users.update_one(
            {"_id": user_id_object},
            {"$set": update_data}
        )
        if result.matched_count == 0:
            raise ValueError("User not found")

        if request.is_json:
            return jsonify({"message": "Profile updated successfully"}), 200
        else:
            flash("Profile updated successfully!")
            return redirect(url_for("profile.index"))

    except Exception as e:
        print("Error:", e)
        if request.is_json:
            return jsonify({"error": str(e)}), 500
        else:
            flash("An error occurred while updating the profile.")
            return redirect(url_for("profile.index"))


@profile.route("/delete", methods=["POST"])
def delete():
    current_user_id = session.get("user_id")
    user_id_object = ObjectId(current_user_id)
    user_device_ids = [device["_id"] for device in db.light_devices.find({"user_id": current_user_id})]

    try:
        # Delete user-related data from other collections
        db.device_files.delete_many({"device_id": {"$in": user_device_ids}}) 
        db.light_devices.delete_many({"user_id": current_user_id})
        db.thermostat_devices.delete_many({"user_id": current_user_id})

        # Delete user from MongoDB
        db.users.delete_one({"_id": user_id_object})

        session.pop("user_id", None)

        if request.is_json:
            return jsonify({"message": "Account deleted successfully"})
        else:
            flash("Account deleted successfully!")
            return redirect(url_for("auth.login"))

    except Exception as e:
        if request.is_json:
            return jsonify({"error": str(e)}), 500
        else:
            flash("An error occurred while deleting the account.")
            return redirect(url_for("profile.index"))

