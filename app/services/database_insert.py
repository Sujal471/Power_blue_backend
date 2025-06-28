from app.db import get_database
from langchain.schema import HumanMessage
dbname = get_database()
collection = dbname["Previous_chats"]
def store_chat(phone_no: str, name: str, user_question: str, ai_response: str):
    """
    Stores chat as a queue of size 30 — pushes new pair and pops oldest if needed.
    """

    chat_pair = [
        {"role": "user", "content": user_question},
        {"role": "ai", "content": ai_response}
    ]

    # Check if user exists
    if collection.find_one({"Phone_no": phone_no}):
        # Push both messages and keep only the last 30 entries
        collection.update_one(
            {"Phone_no": phone_no},
            {
                "$push": {
                    "chat_history": {
                        "$each": chat_pair,
                        "$slice": -60  # Keep only the last 30 items
                    }
                }
            }
        )
    else:
        # If new user, insert chat
        new_user = {
            "Phone_no": phone_no,
            "name": name,
            "chat_history": chat_pair
        }
        collection.insert_one(new_user)

def retrieve_chat_history(phone_no: str):
    """
    Retrieves chat history in format:
    [HumanMessage(...), 'response', HumanMessage(...), 'response', ...]
    """
    doc = collection.find_one({"Phone_no": phone_no})
    if not doc:
        return []

    formatted_history = []
    for item in doc["chat_history"]:
        if item["role"] == "user":
            formatted_history.append(HumanMessage(content=item["content"]))
        elif item["role"] == "ai":
            formatted_history.append(item["content"])
    
    return formatted_history


