import streamlit as st
import google.generativeai as genai
import os
import json
import datetime
import re

# --- Page Config ---
st.set_page_config(
    page_title="Bangkok Travel Bro",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for modern UI ---
st.markdown("""
    <style>
        /* Import fonts */
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap');
        
        /* Main theme */
        :root {
            --primary: #3b82f6;
            --primary-hover: #2563eb;
            --background: #f8fafc;
            --card-bg: #ffffff;
            --text: #1e293b;
            --text-secondary: #64748b;
            --border: #e2e8f0;
            --accent: #3b82f6;
        }
        
        /* Global styling */
        html, body, [class*="css"] {
            font-family: 'DM Sans', sans-serif;
            background-color: var(--background);
            color: var(--text);
        }
        
        /* Main container */
        .main .block-container {
            padding: 1.5rem;
            max-width: 1400px;
        }
        
        /* Headers */
        h1 {
            font-weight: 700;
            color: var(--text);
            font-size: 2.5rem;
            letter-spacing: -0.025em;
            margin-bottom: 0.5rem;
        }
        
        h3 {
            font-weight: 600;
            color: var(--text-secondary);
            margin-bottom: 1.5rem;
        }
        
        /* Card styling */
        .card {
            background-color: var(--card-bg);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
            margin-bottom: 1rem;
            border: 1px solid var(--border);
        }
        
        /* Buttons */
        .stButton > button {
            background-color: var(--primary);
            color: white;
            font-weight: 500;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-size: 1rem;
            transition: all 0.2s ease;
        }
        
        .stButton > button:hover {
            background-color: var(--primary-hover);
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
        }
        
        .secondary-button > button {
            background-color: #f1f5f9;
            color: var(--text);
            border: 1px solid var(--border);
        }
        
        .secondary-button > button:hover {
            background-color: #e2e8f0;
        }
        
        /* Input fields */
        .stTextInput > div > div > input, 
        .stNumberInput > div > div > input {
            border-radius: 8px;
            border: 1px solid var(--border);
            padding: 0.75rem 1rem;
            font-size: 1rem;
        }
        
        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
        }
        
        /* Select boxes */
        .stSelectbox > div > div > div {
            border-radius: 8px;
            border: 1px solid var(--border);
        }
        
        .stSelectbox > div > div > div:focus {
            border-color: var(--primary);
        }
        
        /* Date inputs */
        .stDateInput > div > div > input {
            border-radius: 8px;
            border: 1px solid var(--border);
        }
        
        /* Chat styling */
        .stChatMessage {
            background-color: var(--card-bg);
            border-radius: 12px;
            padding: 1.25rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
            border: 1px solid var(--border);
            margin-bottom: 0.75rem;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 2px;
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 4px 4px 0px 0px;
            padding: 10px 16px;
            background-color: transparent;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: var(--primary);
            color: white;
        }
        
        /* Forms */
        [data-testid="stForm"] {
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }
        
        /* Hide default elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Authentication form */
        .auth-container {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 70vh;
        }
        
        .auth-form {
            width: 100%;
            max-width: 450px;
            background-color: white;
            padding: 2.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            border: 1px solid var(--border);
        }
        
        .app-title {
            font-size: 2.25rem;
            font-weight: 700;
            background: linear-gradient(90deg, #3b82f6, #0ea5e9);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 0.75rem;
        }
        
        .app-subtitle {
            text-align: center;
            font-size: 1.1rem;
            color: var(--text-secondary);
            margin-bottom: 2rem;
        }
        
        /* Recommendation cards */
        .recommendations {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }
        
        .recommendation-card {
            background-color: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
            border: 1px solid var(--border);
        }
        
        .card-content {
            padding: 1rem;
        }
        
        .card-title {
            font-weight: 600;
            font-size: 1.1rem;
            margin-bottom: 0.5rem;
        }
        
        .card-meta {
            display: flex;
            justify-content: space-between;
            color: var(--text-secondary);
            font-size: 0.9rem;
        }
        
        /* Custom expander */
        .custom-expander {
            border: 1px solid var(--border);
            border-radius: 8px;
            margin-bottom: 0.75rem;
        }
        
        .expander-header {
            padding: 0.75rem 1rem;
            background-color: #f8fafc;
            border-bottom: 1px solid var(--border);
            font-weight: 500;
            cursor: pointer;
        }
        
        .expander-content {
            padding: 1rem;
        }
        
        /* Chat input */
        .chat-input-container {
            margin-top: 1rem;
            border: 1px solid var(--border);
            border-radius: 12px;
            overflow: hidden;
        }
        
        [data-testid="stChatInput"] {
            border-radius: 0;
            border: none;
            padding: 1rem;
        }
        
        /* Container borders */
        [data-testid="stVerticalBlock"] [data-testid="stHorizontalBlock"] [data-testid="element-container"] [data-testid="stVerticalBlock"] {
            border-radius: 12px;
            padding: 1.25rem;
            background-color: white;
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
        return "🌅 Good morning, traveler!"
    elif hour < 18:
        return "☀️ Good afternoon, adventurer!"
    else:
        return "🌃 Good evening, wanderer!"

# --- Auth State ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# --- Store Location in Session State ---
if "location" not in st.session_state:
    st.session_state.location = None

# --- Login/Register Page ---
if not st.session_state.authenticated:
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    st.markdown('<div class="auth-form">', unsafe_allow_html=True)
    
    # App logo and title
    st.markdown('<div class="app-title">Bangkok Travel Bro</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-subtitle">Your AI companion for the perfect Bangkok adventure</div>', unsafe_allow_html=True)
    
    # Login form
    with st.form("login_form"):
        email = st.text_input("📧 Email", placeholder="Enter your email")
        password = st.text_input("🔑 Password", placeholder="Enter password", type="password")
        
        cols = st.columns(2)
        with cols[0]:
            login_submitted = st.form_submit_button("🚪 Login", use_container_width=True)
        with cols[1]:
            register_submitted = st.form_submit_button("📝 Register", use_container_width=True)
    
    # Handle authentication
    if login_submitted:
        if authenticate(email, password):
            st.session_state.authenticated = True
            st.session_state.email = email
            st.success("Welcome back! 🎉")
            st.experimental_rerun()
        else:
            st.error("Invalid email or password")
    
    if register_submitted:
        if not email or not password:
            st.error("Please enter both email and password")
        elif '@' not in email:
            st.error("Please enter a valid email address")
        else:
            save_user(email, password)
            st.success("Registration successful! Please log in.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Main App After Login ---
else:
    # Create two columns - sidebar and main content
    col1, col2 = st.columns([1, 3])
    
    # Sidebar
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f'<h3 style="margin-bottom: 0.5rem; font-size: 1.5rem;">{greet_user()}</h3>', unsafe_allow_html=True)
        st.markdown(f'<p style="color: var(--text-secondary);">Logged in as <strong>{st.session_state.email}</strong></p>', unsafe_allow_html=True)
        st.markdown('<hr style="margin: 1rem 0; border: 0; border-top: 1px solid var(--border);">', unsafe_allow_html=True)
        
        # Location detection
        if st.session_state.location is None:
            st.button("📍 Detect My Location", key="detect_location", on_click=lambda: setattr(st.session_state, "location", {"latitude": 13.7563, "longitude": 100.5018}))
        else:
            st.success(f"📍 Bangkok detected")
        
        st.markdown('<hr style="margin: 1rem 0; border: 0; border-top: 1px solid var(--border);">', unsafe_allow_html=True)
        
        # Trip profile
        st.markdown('#### 🧳 Trip Profile')
        
        if st.button("Sign Out", key="sign_out", on_click=lambda: setattr(st.session_state, "authenticated", False)):
            st.experimental_rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content
    with col2:
        st.markdown('<h1 style="text-align: center;">Plan Your Bangkok Adventure</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: var(--text-secondary); font-size: 1.1rem; margin-bottom: 2rem;">Your personal AI guide to Thailand\'s vibrant capital</p>', unsafe_allow_html=True)
        
        # User context form if not already provided
        if "user_context" not in st.session_state:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("#### 🌍 Tell me about your trip plans:")
            
            with st.form("user_info"):
                col1, col2 = st.columns(2)
                with col1:
                    language = st.selectbox("🌐 Preferred Language", 
                                          ["English 🇬🇧", "Malay 🇲🇾", "Hindi 🇮🇳", "Chinese 🇨🇳"])
                with col2:
                    budget = st.number_input("💰 Your Budget per day (THB)", min_value=1000, value=3000)
                
                col3, col4 = st.columns(2)
                with col3:
                    start_date = st.date_input("🗓 Arrival Date", value=datetime.datetime.now())
                with col4:
                    end_date = st.date_input("🗓 Departure Date", value=datetime.datetime.now() + datetime.timedelta(days=5))
                
                interests = st.multiselect("✨ Your Interests", 
                                         ["Food & Cuisine", "Culture & History", "Shopping", 
                                          "Nightlife", "Nature", "Adventure", "Relaxation"])
                
                submitted = st.form_submit_button("✅ Save Trip Info", use_container_width=True)
                
                if submitted:
                    st.session_state.user_context = {
                        "language": language.split()[0],
                        "budget": budget,
                        "start_date": str(start_date),
                        "end_date": str(end_date),
                        "interests": interests
                    }
                    st.success("All set! Let's plan your perfect trip 🤙")
                    st.balloons()
                    st.experimental_rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Chat interface once user context is provided
        if "user_context" in st.session_state:
            tabs = st.tabs(["💬 Chat", "🗺️ Explore", "📋 Itinerary"])
            
            with tabs[0]:  # Chat tab
                st.markdown("### 💬 Ask me anything about Bangkok:")
                
                # Initialize chat history if not exists
                if "chat_history" not in st.session_state:
                    st.session_state.chat_history = []
                
                # Show chat history expander
                with st.expander("📂 View Previous Conversations", expanded=False):
                    for i, chat in enumerate(reversed(st.session_state.chat_history[-20:]), 1):
                        st.markdown(f"**You:** {chat['user']}")
                        st.markdown(f"**Bro:** {chat['assistant']}")
                        st.markdown('<hr style="margin: 0.75rem 0; border: 0; border-top: 1px solid var(--border);">', unsafe_allow_html=True)
                
                # Display existing conversation
                for chat in st.session_state.chat_history:
                    with st.chat_message("user"):
                        st.write(chat["user"])
                    with st.chat_message("assistant"):
                        st.write(chat["assistant"])
                
                # Chat input
                user_input = st.chat_input("What do you want to know about Bangkok?")
                
                if user_input:
                    context = st.session_state.user_context
                    
                    # Format data for the AI
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
                    
                    # Get recent conversation for context
                    past_chat = ""
                    for chat in st.session_state.chat_history[-6:]:
                        past_chat += f"User: {chat['user']}\nAI Bro: {chat['assistant']}\n"
                    
                    # Location info
                    location_info = ""
                    if st.session_state.location:
                        location_info = f"User current location: Latitude {st.session_state.location['latitude']}, " \
                                        f"Longitude {st.session_state.location['longitude']}\n"
                    else:
                        location_info = "User current location: Not detected yet.\n"
                    
                    # Construct prompt for AI
                    prompt = f"""
You're a helpful and chill AI travel bro for someone visiting Bangkok.
If it's appropriate, show a brief intro paragraph followed by a list of recommendations.
Use this format when showing structured results:
{{"cards": [{{"name": "Name", "price": 250, "rating": 4.3, "location": "Area", "type": "hostel", "button": "Book Now"}}]}}

ONLY use this data when recommending places:
{data_snippet}

User preferences:
- Language: {context['language']}
- Budget: {context['budget']} THB
- Travel Dates: {context['start_date']} to {context['end_date']}
- Interests: {', '.join(context.get('interests', []))}

{location_info}
Chat so far:
{past_chat}

User: {user_input}

Respond in {context['language']}. Be smart, friendly, casual. Keep the flow.
"""
                    
                    # Show user message
                    with st.chat_message("user"):
                        st.write(user_input)
                    
                    # Get AI response
                    with st.chat_message("assistant"):
                        with st.spinner("Finding the perfect recommendations for you... 💭"):
                            response = model.generate_content(prompt)
                            reply = response.text
                            
                            try:
                                # Check if response contains card data
                                card_json_match = re.search(r'\{.*"cards"\s*:\s*\[.*\]\s*\}', reply, re.DOTALL)
                                if card_json_match:
                                    parsed = json.loads(card_json_match.group())
                                    intro_text = reply.split(card_json_match.group())[0].strip()
                                    
                                    if intro_text:
                                        st.write(intro_text)
                                        
                                    # Display cards in a grid
                                    st.markdown("**Here are some recommendations just for you:**")
                                    cols = st.columns(len(parsed["cards"]) if len(parsed["cards"]) <= 3 else 3)
                                    
                                    for i, card in enumerate(parsed["cards"]):
                                        col_idx = i % 3
                                        with cols[col_idx]:
                                            with st.container():
                                                st.markdown(f"##### {card['name']}")
                                                st.markdown(f"**Location:** {card['location']}")
                                                st.markdown(f"**Type:** {card['type'].title()}")
                                                st.markdown(f"**Price:** {card['price']} THB")
                                                st.markdown(f"**Rating:** {card['rating']} ⭐")
                                                st.button(card.get("button", "Select"), key=f"{card['name']}_{i}")
                                else:
                                    st.write(reply)
                            except Exception as e:
                                st.write(reply)
                                st.error(f"Error parsing recommendations: {str(e)}")
                    
                    # Update chat history
                    st.session_state.chat_history.append({
                        "user": user_input,
                        "assistant": reply
                    })
                    
                    # Save conversation
                    save_convo(st.session_state.email, st.session_state.chat_history)
                    st.toast("📂 Conversation saved")
            
            with tabs[1]:  # Explore tab
                st.markdown("### 🗺️ Explore Bangkok")
                
                # Create exploration filters
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    category = st.selectbox("Category", ["All", "Attractions", "Food", "Shopping", "Accommodation"])
                
                with col2:
                    area = st.selectbox("Area", ["All", "Sukhumvit", "Silom", "Old City", "Chinatown", "Riverside"])
                
                with col3:
                    price = st.select_slider("Price Range", options=["$", "$$", "$$$", "$$$$"], value=("$", "$$$"))
                
                # Display exploration results
                st.markdown("#### Popular Places")
                
                # Sample data - would be filtered from your actual data
                sample_places = [
                    {"name": "Grand Palace", "type": "attraction", "location": "Old City", "price": "$$$", "rating": 4.7, 
                     "image": "https://images.unsplash.com/photo-1590656241672-02ef2d7d294f?w=600&auto=format"},
                    {"name": "Chatuchak Weekend Market", "type": "shopping", "location": "North Bangkok", "price": "$", "rating": 4.5,
                     "image": "https://images.unsplash.com/photo-1552465011-b4e21bf6e79a?w=600&auto=format"},
                    {"name": "Thip Samai Pad Thai", "type": "food", "location": "Old City", "price": "$", "rating": 4.8,
                     "image": "https://images.unsplash.com/photo-1632814660196-abc8e302e0b7?w=600&auto=format"}
                ]
                
                # Create place cards
                cols = st.columns(3)
                for i, place in enumerate(sample_places):
                    with cols[i]:
                        st.markdown(f"""
                        <div class="recommendation-card">
                            <img src="{place['image']}" style="width: 100%; height: 180px; object-fit: cover;">
                            <div class="card-content">
                                <div class="card-title">{place['name']}</div>
                                <div style="color: var(--text-secondary); font-size: 0.9rem; margin-bottom: 0.5rem;">
                                    {place['location']} • {place['type'].title()} • {place['price']}
                                </div>
                                <div style="display: flex; justify-content: space-between; align-items: center;">
                                    <span>⭐ {place['rating']}</span>
                                    <span>→ Details</span>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            
            with tabs[2]:  # Itinerary tab
                st.markdown("### 📋 Your Bangkok Itinerary")
                st.info("Your personalized itinerary will appear here as you plan your trip.")
                
                # Sample itinerary day
                st.markdown("#### Day 1: Cultural Immersion")
                
                with st.expander("Morning"):
                    st.markdown("""
                    - **08:00 AM** - Breakfast at hotel
                    - **09:30 AM** - Visit Grand Palace & Wat Phra Kaew
                    - **12:00 PM** - Lunch at nearby riverside restaurant
                    """)
                
                with st.expander("Afternoon"):
                    st.markdown("""
                    - **01:30 PM** - Explore Wat Pho (Reclining Buddha)
                    - **03:00 PM** - Cross river to Wat Arun
                    - **04:30 PM** - Tuk-tuk ride to Khao San Road
                    """)
                
                with st.expander("Evening"):
                    st.markdown("""
                    - **06:00 PM** - Dinner at local street food vendors
                    - **08:00 PM** - Rooftop bar for drinks with skyline view
                    - **10:00 PM** - Return to hotel
                    """)
                
                # Add new day button
                st.button("+ Add Day to Itinerary", key="add_day")
