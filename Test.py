from AI import authenticate_gmail
from db import extract_contacts_from_db_by_uid

uid = 'kJRoumGMSsfUKLoxkUqv8kL6YCn2'

contacts = extract_contacts_from_db_by_uid(uid)

if contacts:
    for contact in contacts:
        print(f" {contact['name']}, Email: {contact['email']}")
else:
    print(f"No contacts found for UID {uid}.")