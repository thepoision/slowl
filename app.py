import streamlit as st
import google.generativeai as genai
import os
import json
import datetime
import re

# --- Page Config ---
st.set_page_config(page_title="Bangkok Travel Bro", page_icon="🧲", layout="centered")
st.markdown("""
    <style>
        html, body, [class*="css"]  {
            font-family: 'Segoe UI', sans-serif;
            background-color: #f7f8fa;
        }
        h1, h3 {
            color: #1f2937;
        }
        .stButton > button {
            background-color: #3b82f6;
            color: white;
            border-radius: 10px;
            padding: 0.5em 1em;
            font-weight: bold;
        }
        .stButton > button:hover {
            background-color: #2563eb;
        }
        .stMarkdown, .stTextInput, .stSelectbox, .stNumberInput, .stDateInput {
            padding: 0.3em;
        }
        .stChatMessage {
            border-radius: 12px;
            background-color: #ffffff;
            padding: 1em;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.03);
        }
    </style>
""", unsafe_allow_html=True)

# --- Gemini Flash 2.0 API Key ---
genai.configure(api_key="AIzaSyD3eVlWuVn1dYep2XOW3OaI6_g6oBy38Uk")
model = genai.GenerativeModel("gemini-2.0-flash")

# --- Load Bangkok Data ---
@st.cache_data
def load_data():
    with open("bangkok_data.json", "r") as f:
        return json.load(f)

local_data = load_data()

# --- Load Bangkok Map Data ---
@st.cache_data
def load_map_data():
    with open("bangkok_map.json", "r") as f:
        return json.load(f)

map_data = load_map_data()

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

# --- Auth State ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# --- Store Location in Session State ---
if "location" not in st.session_state:
    st.session_state.location = None

# --- Login/Register Page ---
if not st.session_state.authenticated:
    with st.container():
        st.markdown("""
            <h1 style='text-align: center;'>🧲 Bangkok Travel Bro</h1>
            <p style='text-align: center;'>🚀 Sign in to start planning your Bangkok adventure!</p>
        """, unsafe_allow_html=True)

        with st.form("auth_form"):
            st.text_input("📧 Email", placeholder="Enter your email", key="email")
            st.text_input("🔑 Password", placeholder="Enter password", type="password", key="password")
            col1, col2 = st.columns(2)
            with col1:
                login_btn = st.form_submit_button("🚪 Login")
            with col2:
                register_btn = st.form_submit_button("📝 Register")

    if login_btn:
        if authenticate(st.session_state.email, st.session_state.password):
            st.session_state.authenticated = True
            st.session_state.email = st.session_state.email
            st.success("You're in, bro! 🎉")
        else:
            st.error("Wrong email or password 💀")

    if register_btn:
        save_user(st.session_state.email, st.session_state.password)
        st.success("Boom. You're registered. Now log in! 🔓")

# --- Main App After Login ---
else:
    with st.container():
        st.markdown(f"""
            <h1 style='text-align: center;'>🏕️ Plan Your Trip With Your AI Bro</h1>
            <h3 style='text-align: center;'>{greet_user()}</h3>
            <hr>
        """, unsafe_allow_html=True)

    if st.session_state.location is None:
        if st.button("📍 Detect My Current Location"):
            st.session_state.location = {"latitude": 13.7563, "longitude": 100.5018}
            st.success(f"Location detected: {st.session_state.location['latitude']}, {st.session_state.location['longitude']}")
