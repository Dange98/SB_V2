import streamlit as st
import bcrypt
import json
import os
import uuid
from datetime import datetime
import openai

# --- Config ---
ALLOW_ANY_EMAIL = True  # Change to False to allow only UTA emails

# Database file
DB_FILE = "data/users.json"

st.title("📝 Register for StudyBuddy V2")

# Input fields
email = st.text_input("Enter your email")
password = st.text_input("Create a password", type="password")

# Load or initialize user database
if os.path.exists(DB_FILE):
    with open(DB_FILE, "r") as f:
        users = json.load(f)
else:
    users = {}

# --- Handle Registration ---
if st.button("Register"):
    if not email or not password:
        st.error("Please fill in both email and password.")

    elif not ALLOW_ANY_EMAIL:
        if not (email.endswith("@uta.edu") or email.endswith("@mavs.uta.edu")):
            st.error("Only UTA email addresses are allowed for registration.")

    elif email in users:
        st.error("This email is already registered. Please go to the Login page.")

    else:
        # Hash the password
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        # Create a unique token
        token = "stu_" + uuid.uuid4().hex[:8]

        # Create a personal OpenAI thread for the student
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        thread = client.beta.threads.create()

        # Save user data
        users[email] = {
            "password_hash": hashed_pw,
            "token": token,
            "thread_id": thread.id,
            "created_at": str(datetime.utcnow())
        }

        with open(DB_FILE, "w") as f:
            json.dump(users, f, indent=4)

        st.success("🎉 Registration successful! Please go to the Login page to sign in.")
