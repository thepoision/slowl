import streamlit as st
st.set_page_config(page_title="Bangkok Travel Bro", page_icon="🧲", layout="centered")

import google.generativeai as genai
import os
import json
import datetime
import re

# --- Inject Custom CSS for Modern UI ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
        background-color: #f5f7fa;
        color: #1f2937;
    }

    h1, h2, h3 {
        color: #111827;
    }

    .stButton button {
        background: linear-gradient(to right, #00b4d8, #0077b6);
        color: white;
        padding: 0.6rem 1.2rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    .stButton button:hover {
        transform: scale(1.05);
    }

    div[data-testid="stChatInput"] textarea {
        border: 2px solid #0077b6;
        border-radius: 10px;
        padding: 10px;
    }

    .stContainer {
        border-radius: 12px;
        padding: 20px;
        background: white;
        box-shadow: 0 2px 12px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
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

# === The rest of your logic remains unchanged ===
# (Login/Register, Trip Info, Chat UI, Gemini integration, etc.)

# ✨ From here onward, everything continues as before.
# (Let me know if you want a modern layout for specific parts like trip form or chat cards!)
