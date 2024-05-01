from functools import wraps
from flask import request, jsonify, current_app, abort
import jwt
from pymongo import MongoClient
from bson import ObjectId

# MongoDB connection
client = MongoClient(
    "mongodb://localhost:27017/"
)  # Assuming MongoDB is running locally on the default port
db = client.smart_home  # Accessing the "smart_home" database
users_collection = db.users  # Accessing the "users" collection


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get("auth_token")

        if not token:
            abort(401)

        try:
            data = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )
            current_user = users_collection.find_one(
                {"_id": ObjectId(data["public_id"])}
            )
            if not current_user:
                abort(403)
        except jwt.ExpiredSignatureError:
            abort(401)
        except jwt.InvalidTokenError:
            abort(403)

        return f(current_user, *args, **kwargs)

    return decorated
