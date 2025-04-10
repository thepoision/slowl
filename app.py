import streamlit as st
import google.generativeai as genai
import os
import json
from datetime import datetime

# Setup API
genai.configure(api_key="YOUR_API_KEY_HERE")
model = genai.GenerativeModel("gemini-2.0-flash")

# Load user DB (for demo)
USER_DB_PATH = "users.json"
if not os.path.exists(USER_DB_PATH):
    with open(USER_DB_PATH, "w") as f:
        json.dump({}, f)

# Load or save users
def load_users():
    with open(USER_DB_PATH, "r") as f:
        return json.load(f)

def save_user(email, password):
    users = load_users()
    users[email] = {"password": password}
    with open(USER_DB_PATH, "w") as f:
        json.dump(users, f)

# Authenticate user
def authenticate(email, password):
    users = load_users()
    return email in users and users[email]["password"] == password

# Save conversation
def save_convo(email, convo):
    os.makedirs("chat_logs", exist_ok=True)
    filename = f"chat_logs/{email.replace('@','_at_')}.json"
    history = []
    if os.path.exists(filename):
        with open(filename, "r") as f:
            history = json.load(f)
    history.append({"timestamp": str(datetime.now()), "chat": convo})
    with open(filename, "w") as f:
        json.dump(history, f, indent=2)

# App State
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Login / Register UI
if not st.session_state.authenticated:
    st.title("🔐 Login or Register")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    login_btn = st.button("Login")
    register_btn = st.button("Register")

    if login_btn:
        if authenticate(email, password):
            st.session_state.authenticated = True
            st.session_state.email = email
            st.success("Logged in!")
        else:
            st.error("Invalid credentials")

    if register_btn:
        save_user(email, password)
        st.success("Registered. You can now login.")

else:
    # Chat UI
    st.title("🌆 Bangkok Travel Assistant")
    st.markdown("Let's plan your Bangkok trip!")

    # User context input
    if "user_context" not in st.session_state:
        with st.form("user_info"):
            language = st.selectbox("Preferred Language", ["English", "Malay", "Hindi", "Chinese"])
            budget = st.number_input("Your total budget (in THB)", min_value=1000)
            start_date = st.date_input("Start Date")
            end_date = st.date_input("End Date")
            submit = st.form_submit_button("Submit")

            if submit:
                st.session_state.user_context = {
                    "language": language,
                    "budget": budget,
                    "start_date": str(start_date),
                    "end_date": str(end_date),
                }
                st.success("Preferences saved! Start chatting below 👇")

    if "user_context" in st.session_state:
        st.markdown("### 💬 Chat with your AI travel assistant")
        user_input = st.chat_input("Ask anything about Bangkok...")

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        if user_input:
            # Prepare context-aware prompt
            context = st.session_state.user_context
            prompt = f"""
            You are an AI travel assistant. The user is traveling to Bangkok.
            Here are the user details:
            - Language: {context['language']}
            - Budget: {context['budget']} THB
            - Travel Dates: {context['start_date']} to {context['end_date']}

            Respond in {context['language']} and provide helpful suggestions or answers.

            User: {user_input}
            """

            with st.spinner("Thinking..."):
                response = model.generate_content(prompt)
                reply = response.text

            st.chat_message("user").write(user_input)
            st.chat_message("assistant").write(reply)

            st.session_state.chat_history.append({"user": user_input, "assistant": reply})

            # Save chat
            save_convo(st.session_state.email, st.session_state.chat_history)
