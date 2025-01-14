from flask import Flask, render_template, request, redirect, jsonify
from db import add_contacts_to_db
from AI import *

app = Flask(__name__)

contacts = []
conversation_words = []

@app.route('/', methods=['POST'])
def executeCommand():
    uid = request.args.get('uid')
    global conversation_words  # Explicitly declare global variable to avoid scoping issues
        
    try:
        json_data = request.json
    except Exception as e:
        return jsonify({"error": "Invalid JSON format", "message": str(e)}), 400
    
    segments = json_data['segments']

    for segment in segments:
        text = segment.get('text', '')
        if text:  # Only process non-empty text
            words = text.split()
            conversation_words.extend(words)
            if len(conversation_words) > 20:
                conversation_words = conversation_words[-10:]

    full_conversation = " ".join(conversation_words)
    print(f"Updated Full Conversation: {full_conversation}")

    processCommand(full_conversation, uid)
    print("Message sent")
    
    return jsonify({"success": True, "full_conversation": full_conversation}), 200

@app.route("/home", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        uid = request.form["uid"]
        new_contact = {"uid": uid, "name": name, "email": email}

        contacts.append(new_contact)
        add_contacts_to_db([new_contact])

        print(contacts)

        return redirect("/")

    return render_template("index.html", contacts=contacts)


if __name__ == "__main__":
    app.run(debug=True)
