from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

users_memory = {}

def generate_reply(user_id, message):
    if user_id not in users_memory:
        users_memory[user_id] = {"messages": [], "preferences": {}}
    users_memory[user_id]["messages"].append(message)

    reply = f"אמא אומרת 🌸: קיבלתי את ההודעה שלך '{message}'"

    preferences = users_memory[user_id]["preferences"]
    if "engineer" in preferences.get("occupation", ""):
        reply += " – אני זוכרת שאתה מהנדס, אז אני מתמקדת בתשובות פרקטיות."
    if "female" in preferences.get("gender", ""):
        reply += " 💜"
    
    return reply

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_id = data.get("user_id", "guest")
    message = data.get("message", "")
    reply = generate_reply(user_id, message)
    return jsonify({"reply": reply, "memory": users_memory[user_id]["messages"]})

@app.route("/set_preferences", methods=["POST"])
def set_preferences():
    data = request.json
    user_id = data.get("user_id", "guest")
    preferences = data.get("preferences", {})
    if user_id not in users_memory:
        users_memory[user_id] = {"messages": [], "preferences": {}}
    users_memory[user_id]["preferences"].update(preferences)
    return jsonify({"status": "preferences updated", "preferences": users_memory[user_id]["preferences"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
