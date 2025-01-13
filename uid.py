from flask import Flask, request, jsonify
from AI import *
from db import extract_email_from_db_by_uid
from db import extract_contacts_from_db_by_uid_and_name

app = Flask(__name__)

@app.route('/', methods=['POST'])
def memory_creation():
    uid = request.args.get('uid')  # Fetch the UID from the request
    if not uid:
        return jsonify({"status": "error", "message": "No UID provided"}), 400

    print(f"Received memory for UID: {uid}")

    creds = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)
    sender = extract_email_from_db_by_uid(uid)
    input = "send an email to bariq, Lets meet tomorrow at 7 pm IST online for the project discussion"


    email_details = generate_email_details(input)
    
    status = email_details["status"]
    if status == "Success":
        name = email_details['to']
        recipient = extract_contacts_from_db_by_uid_and_name(uid,name)
        subject = email_details["subject"]
        body = email_details["body"]
    message = create_message(sender, recipient, subject, body)
    send_message(service, 'me', message)
    return jsonify({"status": "success", "uid": uid}), 200

    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
