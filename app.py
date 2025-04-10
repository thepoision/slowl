import streamlit as st
import google.generativeai as genai
import os
import json
import datetime

# --- Setup Gemini API ---
genai.configure(api_key="AIzaSyD3eVlWuVn1dYep2XOW3OaI6_g6oBy38Uk")  # Replace with your real API key
model = genai.GenerativeModel("gemini-2.0-flash")

# --- User Database Setup ---
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

# --- Chat Logging ---
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

# --- Streamlit Setup ---
st.set_page_config(page_title="Bangkok Travel Bro", page_icon="🧢")

# --- Auth Flow ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🧢 Bangkok Travel Bro Login")
    st.markdown("Login or Register to plan your epic trip 🌍")
    email = st.text_input("📧 Email")
    password = st.text_input("🔑 Password", type="password")
    login_btn = st.button("🚪 Login")
    register_btn = st.button("📝 Register")

    if login_btn:
        if authenticate(email, password):
            st.session_state.authenticated = True
            st.session_state.email = email
            st.success("You're in, bro! 🎉")
        else:
            st.error("Oops, wrong credentials 💀")

    if register_btn:
        save_user(email, password)
        st.success("You're all set! Now login and let’s goooo 🚀")

else:
    # --- Main Travel Planner ---
    st.title("🛫 Bangkok Travel Bro 🧢")
    st.markdown(f"### {greet_user()} Let's get your trip lit 🔥")

    if "user_context" not in st.session_state:
        with st.form("user_info"):
            language = st.selectbox("🌍 Pick your language, legend:", 
                                    ["English 🇬🇧", "Malay 🇲🇾", "Hindi 🇮🇳", "Chinese 🇨🇳"])
            budget = st.number_input("💸 Your total budget (in THB)", min_value=1000)
            start_date = st.date_input("🗓️ Start Date")
            end_date = st.date_input("🗓️ End Date")
            submit = st.form_submit_button("Save & Start Chat 💬")

            if submit:
                st.session_state.user_context = {
                    "language": language.split()[0],
                    "budget": budget,
                    "start_date": str(start_date),
                    "end_date": str(end_date),
                }
                st.success("Preferences saved! Let’s goooo 🎉")
                st.balloons()

    if "user_context" in st.session_state:
        st.markdown("### 🧠 Ask me anything about Bangkok:")
        user_input = st.chat_input("Yo bro, what’s on your travel mind?")

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        if user_input:
            context = st.session_state.user_context

            prompt = f"""
You're a super chill and helpful AI travel bro helping someone plan their trip to Bangkok.

User details:
- Language: {context['language']}
- Budget: {context['budget']} THB
- Travel Dates: {context['start_date']} to {context['end_date']}

Respond in {context['language']}. Be friendly, drop light jokes, sound like a local buddy. 
Suggest cool places, street food, budget hacks, nightlife — anything they ask. Make it fun but helpful.

User: {user_input}
"""

            with st.spinner("Your AI bro is thinking... 🤔"):
                response = model.generate_content(prompt)
                reply = response.text

            st.chat_message("user").write(user_input)
            st.chat_message("assistant").write(reply)

            st.session_state.chat_history.append({
                "user": user_input,
                "assistant": reply
            })

            save_convo(st.session_state.email, st.session_state.chat_history)
            st.toast("💾 Chat saved!")
