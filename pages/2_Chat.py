import streamlit as st
import openai
import os
import time

# --- Protect: Only show Chatbot page if logged in ---
if "email" not in st.session_state:
    st.session_state.force_login_message = True  # Set a flag to show error on Login page
    st.switch_page("pages/1_Login.py")

# --- Load OpenAI API Key and Assistant ID ---
openai.api_key = st.secrets["OPENAI_API_KEY"]
client = openai.OpenAI()
assistant_id = st.secrets["ASSISTANT_ID"]

# --- Title and Welcome ---
st.title("📚 StudyBuddy V2 Chatbot")
st.write(f"Hello, {st.session_state.email}! 👋 Ready to continue your [SUBJECT] journey? 🚀")

# --- Top Row Buttons: Clear Chat (left) and Sign Out (right) ---
left_col, spacer, right_col = st.columns([2, 6, 2])

with left_col:
    if st.button("🧹 Clear Chat", use_container_width=True):
        st.session_state.messages = []  # Clear chat history

with right_col:
    if st.button("🚪 Sign Out", use_container_width=True):
        # Set logout flag
        st.session_state.logout_message = True  # ✅ Set flag before clearing
        # Clear session variables
        if "email" in st.session_state:
            del st.session_state.email
        if "token" in st.session_state:
            del st.session_state.token
        if "thread_id" in st.session_state:
            del st.session_state.thread_id
        if "messages" in st.session_state:
            del st.session_state.messages
        # Redirect back to Login
        st.switch_page("pages/1_Login.py")


# --- Initialize chat history if not already done ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display previous chat messages ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Central Text Input Box ---
st.markdown("---")  # horizontal separator for neatness

prompt = st.chat_input("Ask your StudyBuddy V2 something about [SUBJECT]!")

# --- Handle New User Message ---
if prompt:
    # Store user message locally
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Send user message to OpenAI Assistant inside student's personal thread
    thread_id = st.session_state.thread_id

    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=prompt
    )

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions=st.secrets["INSTRUCTIONS"]
    )

    while run.status != 'completed':
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )

    messages = client.beta.threads.messages.list(thread_id=thread_id)

    assistant_messages_for_run = [
        message for message in messages
        if message.run_id == run.id and message.role == "assistant"
    ]

    for message in assistant_messages_for_run:
        response = message.content[0].text.value
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
