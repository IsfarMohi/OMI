import os 
from supabase import create_client

url = "https://lynonbmmglvpivolqyrw.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imx5bm9uYm1tZ2x2cGl2b2xxeXJ3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzUzNTU3MTMsImV4cCI6MjA1MDkzMTcxM30.pYR2Aquu9zmWUSPUt5g5nXvoV1DD2Ba8L7Jh7P7XFWQ"
supabase = create_client(url, key)


def add_contacts_to_db(contacts):
    """
    Add users and their contacts to the database.
    :param contacts: List of dictionaries with keys 'uid', 'name', 'email'
    """
    try:
        for contact in contacts:
            uid = contact["uid"]
            name = contact["name"].strip()
            email = contact["email"].strip()

            # Check if the user exists in the Users table
            user_check = supabase.table("user_data").select("*").eq("uid", uid).execute()

            if not user_check.data:  # User does not exist
                # Insert the user into the Users table
                supabase.table("user_data").insert({"uid": uid, "name": name, "email": email}).execute()

            # Check if the contact already exists in contacts_data
            contact_check = (
                supabase.table("contacts_data")
                .select("*")
                .eq("uid", uid)
                .eq("email", email)
                .execute()
            )

            if not contact_check.data:  # Contact does not exist
                # Insert the contact into the contacts_data table
                supabase.table("contacts_data").insert({"uid": uid, "name": name, "email": email}).execute()

        print("Contacts added/updated successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

def extract_contacts_from_db_by_uid(uid):
    """
    Retrieve all contacts with a specific UID from the contacts_data table.
    :param uid: The user ID to filter contacts by.
    :return: List of dictionaries containing contact details (name, email).
    """
    try:
        # Query the contacts_data table for all records where UID matches the provided uid
        response = supabase.table("contacts_data").select("name, email").eq("uid", uid).execute()
        
        if response.data:
            print(f"Contacts for UID {uid} retrieved successfully.")
            return response.data  # Return the list of contact dictionaries (name, email)
        else:
            print(f"No contacts found for UID {uid}.")
            return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def extract_email_from_db_by_uid(uid):
    """
    Retrieve the email of a user by their UID from the user_data table.
    :param uid: The user ID to look up.
    :return: Email as a string or None if not found.
    """
    try:
        response = supabase.table("user_data").select("email").eq("uid", uid).execute()
        if response.data:
            # Assuming only one record is returned per UID
            return response.data[0]['email']
        else:
            print(f"No email found for UID {uid}.")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def extract_contacts_from_db_by_uid_and_name(uid, name):
    """
    Retrieve the email of a contact by UID and name from the contacts_data table.
    :param uid: The user ID to filter contacts by.
    :param name: The name of the contact.
    :return: Email as a string or None if not found.
    """
    try:
        response = supabase.table("contacts_data").select("email").eq("uid", uid).eq("name", name).execute()
        if response.data:
            # Assuming only one record is returned per UID and name
            return response.data[0]['email']
        else:
            print(f"No contact found for UID {uid} and Name {name}.")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

