import streamlit as st
st.set_page_config(page_title="Bangkok Travel Bro", page_icon="🧢", layout="centered")

import google.generativeai as genai
import os
import json
import datetime
import re
import folium
from streamlit_folium import folium_static
from geopy.distance import geodesic
import random

# --- Gemini Flash 2.0 API Key ---
genai.configure(api_key="AIzaSyD3eVlWuVn1dYep2XOW3OaI6_g6oBy38Uk")
model = genai.GenerativeModel("gemini-2.0-flash")

# --- Load Bangkok Data ---
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

# --- Direction Functions ---
def get_coords_from_name(place_name, location_area, data):
    """Extract coordinates for a place from your Bangkok data"""
    # Search through your data for matching place
    for category, items in data.items():
        for item in items:
            if item.get('name') == place_name:
                # In a real implementation, you'd have coordinates in your data
                if 'coordinates' in item:
                    return item['coordinates']
                # Generate fake coordinates near Bangkok
                return [13.7500 + (random.random() * 0.1), 100.5000 + (random.random() * 0.1)]
    
    # Default coordinates in central Bangkok if not found
    return [13.7500, 100.5000]

def get_travel_details(origin, destination, mode="transit"):
    """
    Get detailed travel information between two points in Bangkok
    Returns travel time, distance, steps, and recommended method
    """
    # Calculate direct distance
    direct_distance = geodesic(origin, destination).kilometers
    
    # Determine best transport method based on distance
    if direct_distance < 1:
        recommended_method = "walking"
        estimated_time = direct_distance * 15  # ~15 min per km walking
    elif direct_distance < 5:
        recommended_method = "tuk-tuk or taxi"
        estimated_time = 10 + (direct_distance * 3)  # Base + time per km
    elif direct_distance < 10:
        recommended_method = "BTS Skytrain or MRT"
        estimated_time = 15 + (direct_distance * 2)  # Including walking to/from stations
    else:
        recommended_method = "taxi or Grab"
        estimated_time = direct_distance * 2.5  # Including traffic
    
    # Create travel details
    travel_info = {
        "origin": origin,
        "destination": destination,
        "distance_km": round(direct_distance, 1),
        "estimated_time_mins": round(estimated_time),
        "recommended_method": recommended_method,
        "cost_estimate": estimate_travel_cost(direct_distance, recommended_method),
        "steps": generate_travel_steps(origin, destination, recommended_method)
    }
    
    return travel_info

def estimate_travel_cost(distance, method):
    """Estimate travel cost based on distance and method"""
    if method == "walking":
        return 0
    elif method == "tuk-tuk or taxi":
        return max(50, round(35 + (distance * 8)))  # Base + per km
    elif method == "BTS Skytrain or MRT":
        return max(16, min(44, round(16 + (distance * 3))))  # Min 16, Max 44 THB
    else:  # Taxi for longer distances
        return round(35 + (distance * 5.5))  # Base + per km

def generate_travel_steps(origin, destination, method):
    """Generate step-by-step directions based on transport method"""
    steps = []
    
    if method == "walking":
        steps = [
            f"Start walking from your location",
            f"Continue approximately {round(geodesic(origin, destination).kilometers, 1)} km",
            f"You'll arrive at your destination in about {round(geodesic(origin, destination).kilometers * 15)} minutes"
        ]
    
    elif method == "tuk-tuk or taxi":
        steps = [
            f"Find a tuk-tuk or taxi near your location",
            f"Show the driver this destination: '{get_location_name(destination)}'",
            f"Expected travel time: {round(geodesic(origin, destination).kilometers * 3)} minutes",
            f"Expected cost: {estimate_travel_cost(geodesic(origin, destination).kilometers, method)} THB"
        ]
    
    elif method == "BTS Skytrain or MRT":
        # This would typically involve finding nearest stations
        # Simplified version:
        steps = [
            f"Walk to the nearest BTS/MRT station (use the app to find it)",
            f"Take the train toward {get_direction_between_points(origin, destination)}",
            f"Exit at the station nearest to your destination",
            f"Walk approximately 5-10 minutes to your final destination"
        ]
    
    else:  # Taxi for longer distances
        steps = [
            f"Use the Grab app or hail a taxi",
            f"Show the driver this destination: '{get_location_name(destination)}'",
            f"Expected travel time: {round(geodesic(origin, destination).kilometers * 2.5)} minutes including traffic",
            f"Expected cost: {estimate_travel_cost(geodesic(origin, destination).kilometers, method)} THB"
        ]
    
    return steps

def get_location_name(coords):
    """Return a location name for coordinates - in production this would look up in your data"""
    # Placeholder implementation
    for category, items in local_data.items():
        for item in items:
            if 'coordinates' in item and item['coordinates'] == coords:
                return item['name']
    return "Your destination"

def get_direction_between_points(origin, destination):
    """Return cardinal direction between points"""
    if destination[0] > origin[0]:
        ns = "North"
    else:
        ns = "South"
        
    if destination[1] > origin[1]:
        ew = "East"
    else:
        ew = "West"
        
    return f"{ns}-{ew}"

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
    st.markdown("<h1 style='text-align: center;'>🏕️ Plan Your Trip With Your AI Bro</h1>", unsafe_allow_html=True)
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
                
            # Add location input
            user_location = st.text_input("📍 Where are you staying? (Hotel or area in Bangkok)", 
                                         placeholder="e.g., Khao San Road, Sukhumvit, etc.")

            submitted = st.form_submit_button("✅ Save Trip Info")

            if submitted:
                # Default coordinates for Khao San Road if user doesn't specify
                default_coords = [13.7594, 100.4989]
                
                # Try to find coordinates for user's location
                user_coords = default_coords
                for category, items in local_data.items():
                    for item in items:
                        if user_location.lower() in item.get('name', '').lower() or user_location.lower() in item.get('location', '').lower():
                            if 'coordinates' in item:
                                user_coords = item['coordinates']
                                break
                
                st.session_state.user_context = {
                    "language": language.split()[0],
                    "budget": budget,
                    "start_date": str(start_date),
                    "end_date": str(end_date),
                    "location": user_location,
                    "coordinates": user_coords
                }
                st.success("All set! Let's chat 🤙")
                st.balloons()

    if "user_context" in st.session_state:
        st.markdown("### 💬 Ask me anything about Bangkok:")

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        with st.expander("📂 View Prev. Convo", expanded=False):
            for i, chat in enumerate(reversed(st.session_state.chat_history[-20:]), 1):
                st.markdown(f"**{i}:** {chat['user']}")
                st.markdown(f"<span style='color: gray;'>{i}: {chat['assistant']}</span>", unsafe_allow_html=True)
                st.markdown("---")

        user_input = st.chat_input("Type here, bro...")

        if user_input:
            context = st.session_state.user_context

            def format_data_snippet(data):
                all_items = []
                for category, items in data.items():
                    for item in items:
                        item_info = (
                            f"- {item.get('name', 'Unnamed')} ({item.get('type', 'Unknown').title()}), "
                            f"{item.get('location', 'Unknown')}, Price: {item.get('price', item.get('price_per_night', 'N/A'))}, "
                            f"Rating: {item.get('rating', 'N/A')}, Tags: {', '.join(item.get('tags', []))}"
                        )
                        if 'coordinates' in item:
                            item_info += f", Coordinates: {item['coordinates']}"
                        all_items.append(item_info)
                return "\n".join(all_items)

            data_snippet = format_data_snippet(local_data)

            past_chat = ""
            for chat in st.session_state.chat_history[-6:]:
                past_chat += f"User: {chat['user']}\nAI Bro: {chat['assistant']}\n"

            prompt = f"""
You're a helpful and chill AI travel bro for someone visiting Bangkok.
If it's appropriate, show a brief intro paragraph followed by a list of recommendations.
Use this format when showing structured results:
{{"cards": [{{"name": "Name", "price": 250, "rating": 4.3, "location": "Area", "type": "hostel", "button": "Book Now", "coordinates": [13.7500, 100.5000]}}]}}
Otherwise, respond casually with plain text.

ONLY use this data when recommending places:
{data_snippet}

User preferences:
- Language: {context['language']}
- Budget: {context['budget']} THB
- Travel Dates: {context['start_date']} to {context['end_date']}
- Current Location: {context['location']} (coordinates: {context['coordinates']})

Chat so far:
{past_chat}

User: {user_input}

Respond in {context['language']}. Be smart, friendly, casual. Keep the flow. Decide when to show structured responses. 
If user asks about directions or how to get somewhere, include "coordinates" in your JSON response.
"""

            with st.spinner("Your bro is thinking... 💭"):
                response = model.generate_content(prompt)
                reply = response.text

            st.chat_message("user").markdown(user_input)

            try:
                card_json_match = re.search(r'\{.*"cards"\s*:\s*\[.*\]\s*\}', reply, re.DOTALL)
                if card_json_match:
                    parsed = json.loads(card_json_match.group())
                    intro_text = reply.split(card_json_match.group())[0].strip()
                    if intro_text:
                        st.chat_message("assistant").markdown(intro_text)
                    st.markdown("**Here are some awesome picks for you:**")
                    for card in parsed["cards"]:
                        with st.container(border=True):
                            st.markdown(f"### {card['name']}")
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown(f"**Location:** {card['location']}")
                                st.markdown(f"**Type:** {card['type'].title()}")
                            with col2:
                                st.markdown(f"**Price:** {card['price']} THB")
                                st.markdown(f"**Rating:** {card['rating']} ⭐")
                            
                            # Get destination coordinates
                            dest_coords = card.get('coordinates', get_coords_from_name(card['name'], card['location'], local_data))
                            
                            # Add Travel Directions button
                            if st.button(f"🧭 How to get to {card['name']}", key=f"directions_{card['name']}"):
                                # Get user's current location from context
                                user_loc = context['coordinates']
                                
                                # Get travel details
                                travel_info = get_travel_details(user_loc, dest_coords)
                                
                                # Show the directions in an expander
                                with st.expander(f"🗺️ Directions to {card['name']}", expanded=True):
                                    col1, col2 = st.columns([2, 1])
                                    
                                    with col1:
                                        st.markdown(f"### How to get to {card['name']}")
                                        st.markdown(f"**Distance:** {travel_info['distance_km']} km")
                                        st.markdown(f"**Time:** ~{travel_info['estimated_time_mins']} minutes")
                                        st.markdown(f"**Recommended:** {travel_info['recommended_method']}")
                                        st.markdown(f"**Cost:** ~{travel_info['cost_estimate']} THB")
                                        
                                        st.markdown("### Step-by-step:")
                                        for i, step in enumerate(travel_info['steps'], 1):
                                            st.markdown(f"{i}. {step}")
                                            
                                        # Add Google Maps link
                                        gmaps_url = f"https://www.google.com/maps/dir/?api=1&origin={user_loc[0]},{user_loc[1]}&destination={dest_coords[0]},{dest_coords[1]}&travelmode=transit"
                                        st.markdown(f"[Open in Google Maps]({gmaps_url})")
                                    
                                    with col2:
                                        # Show a simple map
                                        m = folium.Map()
                                        folium.Marker(user_loc, tooltip="You are here").add_to(m)
                                        folium.Marker(dest_coords, tooltip=card['name'], icon=folium.Icon(color='red')).add_to(m)
                                        
                                        # Draw a line between points
                                        folium.PolyLine([user_loc, dest_coords], color="blue", weight=2.5, opacity=1).add_to(m)
                                        
                                        # Fit map to markers
                                        m.fit_bounds([user_loc, dest_coords])
                                        folium_static(m)
                            
                            # Original Select button
                            st.button(card.get("button", "Select"), key=card['name'])
                else:
                    st.chat_message("assistant").markdown(reply)
            except Exception as e:
                st.chat_message("assistant").markdown(reply)
                st.error(f"Error processing response: {e}")

            st.session_state.chat_history.append({
                "user": user_input,
                "assistant": reply
            })

            save_convo(st.session_state.email, st.session_state.chat_history)
            st.toast("📂 Saved that convo, bro!")
