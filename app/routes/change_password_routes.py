from flask import Blueprint, request, jsonify
from app.services.User_login import verify_user
from app.services.User_login import update_password
change_password_bp = Blueprint("change_password_bp", __name__)
@change_password_bp.route("/", methods=["POST"])
def change_password():
    data = request.get_json()

    username = data.get("username")
    old_password = data.get("old_password")
    new_password = data.get("new_password")

    if not username or not old_password or not new_password:
        return jsonify({"error": "Username, old password, and new password are required"}), 400

    if not verify_user(username, old_password):
        return jsonify({"error": "Invalid username or password"}), 401

    update_password(username,new_password)

    return jsonify({"message": "Password updated successfully"}), 200
