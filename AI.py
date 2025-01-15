import os
import json
import base64
from openai import OpenAI
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from dotenv import load_dotenv
from db import *

load_dotenv()
SCOPES = os.getenv('SCOPES')
apikey = os.getenv('API_KEY')
client = OpenAI(api_key = apikey)

print('hello')

def authenticate_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw}

def send_message(service, user_id, message):
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print(f"Message sent. Message ID: {message['id']}")
        return message
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

def generate_email_details(user_command):
    function_schema = {
        "name": "generate_email_details",
        "description": """
        You are an AI assistant that generates an email structure based on the given input.
        - Extract the recipient's email from the input and include it under "To".
        - Use the subject provided by the user. If none is provided, generate a concise, relevant subject.
        - Rewrite the body of the email to ensure it is grammatically correct, professional, and polite.
        """,
        "parameters": {
            "type": "object",
            "properties": {
                "to": {
                    "type": "string",
                    "description": "The email address of the recipient."
                },
                "subject": {
                    "type": "string",
                    "description": "The subject of the email. Use the user-provided subject or generate a concise, relevant subject."
                },
                "body": {
                    "type": "string",
                    "description": "The rewritten email body in a professional and grammatically correct tone."
                },
                "status": {
                    "type": "string",
                    "description": "Status indicating if sufficient data was available.",
                    "enum": ["Success", "Not enough data"]
                }
            },
            "required": ["status"]
        }
    }
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates email details based on user input."},
            {"role": "user", "content": user_command}
        ],
        functions=[function_schema],
        function_call={"name": "generate_email_details"}
    )
    
    function_call_data = completion.choices[0].message.function_call
    extracted_data = json.loads(function_call_data.arguments)
    if extracted_data["status"] == "Not enough data":
        return "Not enough data to process this request."
    else:
        return extracted_data


def processCommand(full_text, uid):
    creds = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)
    sender = extract_email_from_db_by_uid(uid)
    input = full_text


    email_details = generate_email_details(input)
    
    status = email_details["status"]
    if status == "Success":
        name = email_details['to']
        recipient = extract_contacts_from_db_by_uid_and_name(uid,name)
        subject = email_details["subject"]
        body = email_details["body"]
    message = create_message(sender, recipient, subject, body)
    send_message(service, 'me', message)
