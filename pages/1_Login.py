import streamlit as st
import bcrypt
import json
import os

# --- Config ---
ALLOW_ANY_EMAIL = True  # Change to False to allow only UTA emails

# Database file
DB_FILE = "data/users.json"

st.title("🔐 Login to StudyBuddy V2")

# --- Immediate Message Handling BEFORE anything else ---
if "force_login_message" in st.session_state:
    st.error("🚨 Please login first to access StudyBuddy V2 Chatbot!")
    del st.session_state.force_login_message

if "logout_message" in st.session_state:
    st.success("✅ You have been signed out successfully. Please login again.")
    del st.session_state.logout_message

if "reset_message" in st.session_state:
    st.success("✅ Password reset successful! Please login using your newly created password.")
    del st.session_state.reset_message

# --- Input fields for login ---
email = st.text_input("Enter your email")
password = st.text_input("Enter your password", type="password")

# --- Load user database ---
if os.path.exists(DB_FILE):
    with open(DB_FILE, "r") as f:
        users = json.load(f)
else:
    users = {}

# --- Buttons Layout (Login + Forgot Password) ---
left_col, spacer, right_col = st.columns([2, 1, 2])

with left_col:
    login_clicked = st.button("Login", use_container_width=True)

with right_col:
    forgot_clicked = st.button("Forgot Password?", use_container_width=True)

# Placeholder for messages
message_placeholder = st.empty()

# --- Handle Login ---
if login_clicked:
    if not email or not password:
        message_placeholder.error("Please fill in both email and password.")

    elif not ALLOW_ANY_EMAIL:
        if not (email.endswith("@uta.edu") or email.endswith("@mavs.uta.edu")):
            message_placeholder.error("Only UTA email addresses are allowed for login.")

    elif email not in users:
        message_placeholder.error("Email not found. Please register first.")

    else:
        stored_hash = users[email]["password_hash"]
        if bcrypt.checkpw(password.encode(), stored_hash.encode()):
            st.session_state.email = email
            st.session_state.token = users[email]["token"]
            st.session_state.thread_id = users[email]["thread_id"]

            # Redirect immediately after successful login
            st.switch_page("pages/2_Chat.py")
        else:
            message_placeholder.error("Incorrect password. If you forgot your password, you can reset it.")

# --- Handle Forgot Password ---
if forgot_clicked:
    st.markdown("---")
    st.subheader("🔑 Reset Your Password")

    new_password = st.text_input("Enter a new password", type="password", key="reset_password")

    if st.button("Reset Password"):
        if not email or not new_password:
            st.error("Please fill in both your email and your new password to reset.")

        elif not ALLOW_ANY_EMAIL:
            if not (email.endswith("@uta.edu") or email.endswith("@mavs.uta.edu")):
                st.error("Only UTA email addresses are allowed for password reset.")

        elif email not in users:
            st.error("No account found with this email. Please register first.")

        else:
            hashed_pw = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
            users[email]["password_hash"] = hashed_pw

            with open(DB_FILE, "w") as f:
                json.dump(users, f, indent=4)

            st.session_state.reset_message = True
            st.experimental_rerun()
