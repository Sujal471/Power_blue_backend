from flask import Blueprint, jsonify,request
from app.db import get_database
from bson import ObjectId
from app.services.User_login import verify_user
history_bp = Blueprint("history_bp", __name__)
db = get_database()
collection = db["Previous_chats"]

def serialize_doc(doc):
    doc['_id'] = str(doc['_id'])
    return doc

@history_bp.route("/", methods=["GET", "POST"])
def get_chat_history():
    print("Ok")
    data=request.json
    
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    if not verify_user(username, password):
        return jsonify({"error": "Invalid username or password"}), 401
    
    all_chats = list(collection.find({}))
    serialized_chats = [serialize_doc(chat) for chat in all_chats]
    return jsonify(serialized_chats)