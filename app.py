import streamlit as st
import google.generativeai as genai
import os
import json
import datetime
import re

# --- Page Configuration with owl theme ---
st.set_page_config(
    page_title="Bangkok Travel Owl",
    page_icon="🦉",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS for a modern, owl-themed, mobile-responsive look ---
st.markdown("""
<style>
    /* Global Styles */
    .main {
        background-color: #f8f9fa;
        color: #212529;
        max-width: 100% !important;
        padding: 1rem;
    }
    
    /* Mobile Responsiveness */
    @media (max-width: 768px) {
        .main {
            padding: 0.5rem;
        }
        .custom-card {
            padding: 15px;
        }
        h1 {
            font-size: 1.5rem !important;
        }
        h3 {
            font-size: 1.2rem !important;
        }
    }
    
    /* Custom Card Styling */
    .custom-card {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        border-left: 4px solid #8B5D33; /* Owl-themed brown */
    }
    
    /* Button Styling */
    .stButton > button {
        background-color: #8B5D33; /* Owl-themed brown */
        color: white;
        border-radius: 20px;
        border: none;
        padding: 8px 16px;
        font-weight: 500;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background-color: #6E4A26; /* Darker brown */
        box-shadow: 0 5px 10px rgba(110, 74, 38, 0.2);
        transform: translateY(-2px);
    }
    
    /* Input Fields */
    .stTextInput input, .stNumberInput input, .stDateInput input {
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        padding: 10px;
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
    }
    
    /* Hide Hamburger Menu and Footer */
    #MainMenu, footer {
        visibility: hidden;
    }
    
    /* Logo Animation */
    .logo-pulse {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    /* Recommendation Card */
    .recommendation-card {
        background-color: white;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
        margin-bottom: 15px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border-left: 3px solid #8B5D33; /* Owl-themed brown */
    }
    
    .recommendation-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.12);
    }
    
    /* Card title */
    .card-title {
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 8px;
        color: #333;
    }
    
    /* Card metadata */
    .card-meta {
        display: flex;
        align-items: center;
        margin-bottom: 10px;
        font-size: 0.9rem;
        flex-wrap: wrap; /* Better for mobile */
    }
    
    /* Location badge */
    .location-badge {
        background-color: #f0f0f0;
        padding: 3px 8px;
        border-radius: 20px;
        margin-right: 10px;
        margin-bottom: 5px; /* For mobile wrapping */
        color: #555;
        font-size: 0.8rem;
    }
    
    /* Type badge */
    .type-badge {
        background-color: #FFF8E8; /* Light owl/wheat color */
        padding: 3px 8px;
        border-radius: 20px;
        color: #8B5D33; /* Owl-themed brown */
        font-size: 0.8rem;
        margin-bottom: 5px; /* For mobile wrapping */
    }
    
    /* Card footer */
    .card-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 10px;
        flex-wrap: wrap; /* Better for mobile */
    }
    
    /* Price tag */
    .price-tag {
        background-color: #E8F0FF;
        color: #0077cc;
        padding: 3px 8px;
        border-radius: 20px;
        font-weight: 500;
        font-size: 0.85rem;
        margin-bottom: 5px; /* For mobile wrapping */
    }
    
    /* Rating stars */
    .rating {
        color: #FFD700;
        font-size: 0.9rem;
    }
    
    /* Colored header */
    .colored-header {
        padding: 15px;
        border-radius: 10px;
        background-color: rgba(139, 93, 51, 0.1); /* Owl-themed brown with opacity */
        border-left: 5px solid #8B5D33; /* Owl-themed brown */
        margin-bottom: 20px;
    }
    
    /* Section divider */
    .section-divider {
        margin: 15px 0;
        border: none;
        height: 1px;
        background-color: #eee;
    }
    
    /* Fixed height chat container */
    .chat-container {
        max-height: 400px;
        overflow-y: auto;
        margin-bottom: 20px;
        padding-right: 10px;
        -ms-overflow-style: none; /* for Internet Explorer, Edge */
        scrollbar-width: none; /* for Firefox */
    }
    
    .chat-container::-webkit-scrollbar {
        display: none; /* for Chrome, Safari, and Opera */
    }
    
    /* Make chat input always visible */
    .stChatInput {
        position: sticky;
        bottom: 0;
        background-color: #f8f9fa;
        padding: 10px 0;
        z-index: 100;
    }
    
    /* Quick prompt buttons container */
    .quick-prompts {
        display: flex;
        overflow-x: auto;
        padding: 10px 0;
        gap: 10px;
        scroll-snap-type: x mandatory;
        -ms-overflow-style: none;
        scrollbar-width: none;
    }
    
    .quick-prompts::-webkit-scrollbar {
        display: none;
    }
    
    /* Prompt button styles */
    .prompt-button {
        background-color: #f0f0f0;
        color: #333;
        border-radius: 20px;
        border: 1px solid #ddd;
        padding: 6px 12px;
        font-size: 0.85rem;
        cursor: pointer;
        transition: all 0.2s;
        white-space: nowrap;
        text-align: center;
    }
    
    .prompt-button:hover {
        background-color: #e0e0e0;
    }
    
    /* Owl-themed elements */
    .owl-icon {
        color: #8B5D33;
        font-size: 1.5rem;
        margin-right: 10px;
    }
    
    /* Owl-themed avatar for chat */
    .owl-avatar {
        background-color: #FFF8E8;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #8B5D33;
        font-weight: bold;
        margin-right: 10px;
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

# --- Custom colored header ---
def colored_header(label, description=None):
    st.markdown(f"""
    <div class="colored-header">
        <h3>{label}</h3>
        {f"<p>{description}</p>" if description else ""}
    </div>
    """, unsafe_allow_html=True)

# --- Clean AI response ---
def clean_response(text):
    # Remove code block syntax from HTML card content
    # This pattern matches code blocks with HTML content inside
    pattern = r'```(?:html)?(.+?)```'
    matches = re.finditer(pattern, text, re.DOTALL)
    
    # We'll collect all the replacements and apply them in order
    replacements = []
    
    for match in matches:
        code_content = match.group(1).strip()
        # If this code block contains recommendation card HTML
        if '<div class="recommendation-card">' in code_content:
            start, end = match.span()
            replacements.append((start, end, code_content))
    
    # Apply replacements in reverse order to maintain string indices
    result = text
    for start, end, replacement in sorted(replacements, reverse=True):
        result = result[:start] + replacement + result[end:]
    
    return result

# --- Login/Register Page ---
if not st.session_state.authenticated:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="logo-pulse">', unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center;'>🦉 Bangkok Travel Owl</h1>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
        
        # Welcome message in a custom card
        st.markdown("""
        <div class="custom-card">
            <h3>Welcome Explorer!</h3>
            <p>Sign in to discover Bangkok's hidden gems, get personalized recommendations, and plan your perfect trip with your wise travel companion.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

        email = st.text_input("📧 Email", placeholder="your.email@example.com")
        password = st.text_input("🔑 Password", placeholder="Enter password", type="password")
        
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        
        col_login, col_register = st.columns(2)
        with col_login:
            login_btn = st.button("🚪 Login", use_container_width=True)
        with col_register:
            register_btn = st.button("📝 Register", use_container_width=True)

    if login_btn:
        if authenticate(email, password):
            st.session_state.authenticated = True
            st.session_state.email = email
            st.success("Welcome back! Let your wise Owl guide you through Bangkok 🦉")
            st.rerun()
        else:
            st.error("Incorrect email or password 🔐")

    if register_btn:
        save_user(email, password)
        st.success("Successfully registered! Please log in to continue 🔓")

# --- Main App After Login ---
else:
    # Header area with dynamic greeting
    col_header1, col_header2 = st.columns([3, 1])
    with col_header1:
        st.markdown(f"<h1>🦉 Bangkok Travel Owl</h1>", unsafe_allow_html=True)
        st.markdown(f"<h4>{greet_user()}</h4>", unsafe_allow_html=True)
    
    with col_header2:
        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.rerun()
    
    # Horizontal divider
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # Location detection with cleaner UI
    if st.session_state.location is None:
        location_col1, location_col2 = st.columns([3, 1])
        with location_col1:
            st.info("📍 Enable location to get nearby recommendations")
        with location_col2:
            if st.button("Detect Location", key="detect_location"):
                st.session_state.location = {"latitude": 13.7563, "longitude": 100.5018}
                st.success("📍 Bangkok, Thailand detected")
                st.rerun()

    # Trip Information Form
    if "user_context" not in st.session_state:
        st.markdown("""
        <div class="custom-card">
            <h3>✈️ Tell us about your trip</h3>
            <p>Help Owl personalize your Bangkok experience</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("user_info", clear_on_submit=False):
            col1, col2 = st.columns(2)
            with col1:
                language = st.selectbox("🌐 Language", 
                                      ["English 🇬🇧", "Malay 🇲🇾", "Hindi 🇮🇳", "Chinese 🇨🇳"])
            with col2:
                budget = st.number_input("💰 Budget (THB)", min_value=1000, value=5000, step=1000)

            col3, col4 = st.columns(2)
            with col3:
                start_date = st.date_input("🗓 From")
            with col4:
                end_date = st.date_input("🗓 To")

            submit_col1, submit_col2 = st.columns([3, 1])
            with submit_col2:
                submitted = st.form_submit_button("Start Planning →", use_container_width=True)

            if submitted:
                st.session_state.user_context = {
                    "language": language.split()[0],
                    "budget": budget,
                    "start_date": str(start_date),
                    "end_date": str(end_date),
                }
                st.balloons()
                st.rerun()

    # Chat Interface
    if "user_context" in st.session_state:
        colored_header("Your Wise Travel Owl", "Ask me anything about Bangkok, from food to sights!")

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        
        if "current_chat" not in st.session_state:
            st.session_state.current_chat = []

        # Two separate tabs - Chat interface and previous conversations
        chat_tab, history_tab = st.tabs(["💬 Chat with Owl", "📜 Previous Conversations"])
        
        with chat_tab:
            # Quick prompt buttons - fixed implementation using regular buttons in columns
            st.write("**Quick Questions:**")
            
            # First row of quick prompts
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🍜 Food recommendations", key="food_btn", use_container_width=True):
                    st.session_state.quick_prompt = "What are the best Thai dishes I should try in Bangkok?"
            with col2:
                if st.button("🏯 Top attractions", key="attractions_btn", use_container_width=True):
                    st.session_state.quick_prompt = "What are the must-visit attractions in Bangkok?"
            with col3:
                if st.button("🛍️ Shopping spots", key="shopping_btn", use_container_width=True):
                    st.session_state.quick_prompt = "Where are the best places to shop in Bangkok?"
            
            # Second row of quick prompts
            col4, col5, col6 = st.columns(3)
            with col4:
                if st.button("🛡️ Safety tips", key="safety_btn", use_container_width=True):
                    st.session_state.quick_prompt = "What are important safety tips for Bangkok?"
            with col5:
                if st.button("🚕 Transportation", key="transport_btn", use_container_width=True):
                    st.session_state.quick_prompt = "How do I get around Bangkok easily?"
            with col6:
                if st.button("💰 Budget tips", key="budget_btn", use_container_width=True):
                    st.session_state.quick_prompt = "How can I travel Bangkok on a budget?"
            
            # Display only the current chat session
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            if st.session_state.current_chat:
                for chat in st.session_state.current_chat:
                    st.chat_message("user").markdown(chat['user'])
                    
                    # Custom owl avatar for the assistant
                    with st.chat_message("assistant", avatar="🦉"):
                        # Clean and display assistant response
                        cleaned_response = clean_response(chat['assistant'])
                        st.markdown(cleaned_response, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Chat input - ensure it's always visible
            st.markdown('<div id="chat-input-anchor"></div>', unsafe_allow_html=True)
            if "quick_prompt" in st.session_state:
                user_input = st.session_state.quick_prompt
                del st.session_state.quick_prompt
                # Process input immediately
                if user_input:
                    # New message from quick prompt
                    st.chat_message("user").markdown(user_input)
                    # Schedule processing for next rerun
                    st.session_state.process_input = user_input
                    st.rerun()
            else:
                user_input = st.chat_input("Ask Owl anything about Bangkok...", key="user_chat_input")
        
        # Previous conversations tab
        with history_tab:
            if st.session_state.chat_history:
                for i, chat in enumerate(reversed(st.session_state.chat_history), 1):
                    with st.expander(f"Chat {i}: {chat['user'][:40]}{'...' if len(chat['user']) > 40 else ''}", expanded=False):
                        st.markdown(f"**You:** {chat['user']}")
                        cleaned_response = clean_response(chat['assistant'])
                        st.markdown(f"**Owl:** {cleaned_response}", unsafe_allow_html=True)
                
                # Button to start a new chat
                if st.button("Start New Chat", key="new_chat_btn"):
                    st.session_state.current_chat = []
                    st.rerun()
            else:
                st.info("No previous conversations yet")

        # Process scheduled input or direct user input
        process_input = None
        if "process_input" in st.session_state:
            process_input = st.session_state.process_input
            del st.session_state.process_input
        elif user_input:
            process_input = user_input
            
        if process_input:
            context = st.session_state.user_context

            def format_data_snippet(data, limit_per_category=5):
                all_items = []
                for category, items in data.items():
                    for item in items[:limit_per_category]:
                        all_items.append(
                            f"- {item.get('name', 'Unnamed')} ({item.get('type', 'Unknown').title()}), "
                            f"{item.get('location', 'Unknown')}, Price: {item.get('price', item.get('price_per_night', 'N/A'))}, "
                            f"Rating: {item.get('rating', 'N/A')}, Tags: {', '.join(item.get('tags', []))}"
                        )
                return "\n".join(all_items)

            data_snippet = format_data_snippet(local_data)

            # Get only the most recent messages from current chat
            past_chat = ""
            for chat in st.session_state.current_chat[-3:]:  # Limit context to last 3 messages
                past_chat += f"User: {chat['user']}\nAI Owl: {chat['assistant']}\n"

            location_info = ""
            if st.session_state.location:
                location_info = f"User current location: Latitude {st.session_state.location['latitude']}, " \
                                f"Longitude {st.session_state.location['longitude']}\n"
            else:
                location_info = "User current location: Not detected yet.\n"

            prompt = f"""
You're a helpful and wise AI travel Owl for someone visiting Bangkok.
If it's appropriate, show a brief intro paragraph followed by a list of recommendations.

IMPORTANT: I need you to format recommendations as HTML cards using this exact structure:

```html
<div class="recommendation-card">
    <div class="card-title">PLACE NAME</div>
    <div class="card-meta">
        <span class="location-badge">📍 AREA NAME</span>
        <span class="type-badge">TYPE</span>
    </div>
    <div class="card-footer">
        <span class="price-tag">฿PRICE THB</span>
        <span class="rating">⭐⭐⭐⭐ RATING</span>
    </div>
</div>
```

ONLY use this data when recommending places:
{data_snippet}

User preferences:
- Language: {context['language']}
- Budget: {context['budget']} THB
- Travel Dates: {context['start_date']} to {context['end_date']}

{location_info}
Chat so far:
{past_chat}

User: {process_input}

Respond in {context['language']}. Be wise, helpful, friendly. Keep the flow natural.
Always sign your responses with a small owl emoticon 🦉
"""
            with st.spinner("Owl is finding wisdom for you... 🦉"):
                response = model.generate_content(prompt)
                reply = response.text

            # Add to both current chat and full history
            new_chat = {
                "user": process_input,
                "assistant": reply
            }
            st.session_state.current_chat.append(new_chat)
            st.session_state.chat_history.append(new_chat)

            save_convo(st.session_state.email, st.session_state.chat_history)
            st.toast("Saved to your travel journal ✅")
            
            # Force reload to display the new chat
            st.rerun()
