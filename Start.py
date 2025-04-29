import streamlit as st

# Set page config
st.set_page_config(page_title="Welcome to StudyBuddy V2!", page_icon=":books:")

# --- Main content ---
st.title("📚 Welcome to StudyBuddy V2!")

st.write("""
Welcome to **StudyBuddy**, your personal AI-powered assistant for mastering **[SUBJECT]**! 🚀

Here, you can:
- Ask questions about concepts
- Get explanations for homework and quizzes
- Practice and prepare for exams
- Strengthen your understanding step-by-step

StudyBuddy V2 is designed to help you learn **clearly, patiently, and interactively**.
""")

# --- Immediately below description: "When you're ready..." + Login Button (no big gap) ---

col1, col2 = st.columns([5, 2])

with col1:
    st.markdown("When you're ready, click below to **Login** and start your journey!")

with col2:
    if st.button("🔐 Login", use_container_width=True):
        st.switch_page("pages/1_Login.py")

# --- Tiny space ---
st.markdown("<br>", unsafe_allow_html=True)

# --- Small Footer for New Students: Text + Register Button ---
footer_col1, footer_col2 = st.columns([5, 2])

with footer_col1:
    st.markdown(
        "New to StudyBuddyBot V2?",
        unsafe_allow_html=True
    )

with footer_col2:
    if st.button("Click here to Register", use_container_width=True):
        st.switch_page("pages/3_Register.py")
