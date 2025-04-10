import streamlit as st
import google.generativeai as genai
import os
import json
import datetime
import pandas as pd

# --- Gemini Flash 2.0 API Key ---
genai.configure(api_key="AIzaSyD3eVlWuVn1dYep2XOW3OaI6_g6oBy38Uk")
model = genai.GenerativeModel("gemini-2.0-flash")

# --- Load Local Bangkok Data ---
@st.cache_data
def load_data():
    with open("bangkok_data.json", "r") as f:
        return json.load(f)

local_data = load_data()

# --- User DB ---
USER_DB_PATH = "users.json"
if not os.path.exists(USER_DB_PATH):
    with open(USER_DB_PATH, "w") as f:
        json.dump({}, f)

def load_users():
    with open(USER_DB_PATH, "r") as f:
        return json.load(f)

def save_user(email, password):
    users = load_users()
    users[email] = {"password": password}
    with open(USER_DB_PATH, "w") as f:
        json.dump(users, f)

def authenticate(email, password):
    users = load_users()
    return email in users and users[email]["password"] == password

# --- Chat Save ---
def save_convo(email, convo):
    os.makedirs("chat_logs", exist_ok=True)
    filename = f"chat_logs/{email.replace('@','_at_')}.json"
    history = []
    if os.path.exists(filename):
        with open(filename, "r") as f:
            history = json.load(f)
    history.append({"timestamp": str(datetime.datetime.now()), "chat": convo})
    with open(filename, "w") as f:
        json.dump(history, f, indent=2)

# --- Greeting Based on Time ---
def greet_user():
    hour = datetime.datetime.now().hour
    if hour < 12:
        return "🌄 Good morning, traveler!"
    elif hour < 18:
        return "☀️ Good afternoon, adventurer!"
    else:
        return "🌙 Evening vibes, wanderer!"

# --- Streamlit Config ---
st.set_page_config(page_title="Bangkok Travel Bro", page_icon="🧢", layout="centered")

# --- Auth State ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# --- Login/Register Page ---
if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align: center;'>🧢 Bangkok Travel Bro</h1>", unsafe_allow_html=True)
    st.markdown("#### 🚀 Sign in to start planning your Bangkok adventure!")

    with st.container():
        email = st.text_input("📧 Email", placeholder="Enter your email")
        password = st.text_input("🔑 Password", placeholder="Enter password", type="password")
        col1, col2 = st.columns(2)
        with col1:
            login_btn = st.button("🚪 Login")
        with col2:
            register_btn = st.button("📝 Register")

    if login_btn:
        if authenticate(email, password):
            st.session_state.authenticated = True
            st.session_state.email = email
            st.success("You're in, bro! 🎉")
        else:
            st.error("Wrong email or password 💀")

    if register_btn:
        save_user(email, password)
        st.success("Boom. You're registered. Now log in! 🔓")

# --- Main App After Login ---
else:
    st.markdown("<h1 style='text-align: center;'>🏝️ Plan Your Trip With Your AI Bro</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>{greet_user()}</h3>", unsafe_allow_html=True)
    st.markdown("---")

    if "user_context" not in st.session_state:
        st.markdown("#### 🌍 Tell me a bit about your trip:")
        with st.form("user_info"):
            col1, col2 = st.columns(2)
            with col1:
                language = st.selectbox("🌐 Preferred Language", 
                                        ["English 🇬🇧", "Malay 🇲🇾", "Hindi 🇮🇳", "Chinese 🇨🇳"])
            with col2:
                budget = st.number_input("💰 Your Budget (THB)", min_value=1000)

            col3, col4 = st.columns(2)
            with col3:
                start_date = st.date_input("📅 Start Date")
            with col4:
                end_date = st.date_input("📅 End Date")

            submitted = st.form_submit_button("✅ Save Trip Info")

            if submitted:
                st.session_state.user_context = {
                    "language": language.split()[0],
                    "budget": budget,
                    "start_date": str(start_date),
                    "end_date": str(end_date),
                }
                st.success("All set! Let’s chat 🤙")
                st.balloons()

    if "user_context" in st.session_state:
        st.markdown("### 💬 Ask me anything about Bangkok:")

        user_input = st.chat_input("Type here, bro...")

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        if user_input:
            context = st.session_state.user_context

            # Format local dataset into readable lines
            def format_data_snippet(data, type_filter=None):
                items = [d for d in data if not type_filter or d['type'] == type_filter]
                return "\n".join([
                    f"- {item['name']}: {item['type'].title()}, {item['location']}, "
                    f"Price: {item['price']}, Rating: {item['rating']}, Tags: {', '.join(item['tags'])}"
                    for item in items
                ])

            data_snippet = format_data_snippet(local_data)

            prompt = f"""
You're a helpful and chill AI travel bro for someone visiting Bangkok.

ONLY use this data when recommending places:

{data_snippet}

User preferences:
- Language: {context['language']}
- Budget: {context['budget']} THB
- Travel Dates: {context['start_date']} to {context['end_date']}

User question: {user_input}

Respond in {context['language']}. Use casual language, drop suggestions, jokes, and street tips.
"""

            with st.spinner("Your bro is thinking... 💭"):
                response = model.generate_content(prompt)
                reply = response.text

            st.chat_message("user").markdown(user_input)
            st.chat_message("assistant").markdown(reply)

            st.session_state.chat_history.append({
                "user": user_input,
                "assistant": reply
            })

            save_convo(st.session_state.email, st.session_state.chat_history)
            st.toast("💾 Saved that convo, bro!")
