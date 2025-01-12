from flask import Flask, render_template, request, redirect
from db import add_contacts_to_db

app = Flask(__name__)

# In-memory storage for contacts
contacts = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        uid = request.form["uid"]
        new_contact = {"uid": uid, "name": name, "email": email}

        # Add the contact to in-memory storage
        contacts.append(new_contact)

        # Add the contact to the database
        add_contacts_to_db([new_contact])

        print(contacts)

        return redirect("/")  # Redirect to avoid form resubmission

    return render_template("index.html", contacts=contacts)


if __name__ == "__main__":
    app.run(debug=True)
