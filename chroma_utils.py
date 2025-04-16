import chromadb
from chromadb.config import Settings
import json
import os
import uuid
import datetime

# ChromaDB setup
def get_chroma_client():
    """Initialize and return a ChromaDB client"""
    client = chromadb.Client(Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory="chroma_db"
    ))
    return client

def initialize_itineraries_collection(force_reset=False):
    """Initialize the itineraries collection"""
    client = get_chroma_client()
    
    # Delete collection if it exists and force_reset is True
    if force_reset and "bangkok_itineraries" in [col.name for col in client.list_collections()]:
        client.delete_collection("bangkok_itineraries")
    
    # Create collection if it doesn't exist
    try:
        collection = client.get_collection("bangkok_itineraries")
        print("Collection already exists.")
    except:
        collection = client.create_collection(
            name="bangkok_itineraries",
            metadata={"description": "Bangkok travel itineraries"}
        )
        print("Created new collection.")
    
    return collection

def load_sample_itineraries(file_path="itineraries.json"):
    """Load sample itineraries from a JSON file"""
    if not os.path.exists(file_path):
        # Create some sample data if file doesn't exist
        sample_itineraries = generate_sample_itineraries()
        with open(file_path, "w") as f:
            json.dump(sample_itineraries, f, indent=2)
    
    with open(file_path, "r") as f:
        return json.load(f)

def generate_sample_itineraries():
    """Generate sample itineraries for initial setup"""
    return [
        {
            "id": str(uuid.uuid4()),
            "title": "Bangkok Highlights - 3 Days",
            "description": "A short but comprehensive tour of Bangkok's most famous attractions",
            "duration": 3,
            "budget_category": "medium",  # low, medium, high
            "budget_amount": 5000,
            "suitable_for": ["solo", "couples", "friends"],
            "days": [
                {
                    "day": 1,
                    "title": "Historic Bangkok",
                    "activities": [
                        {
                            "time": "09:00",
                            "activity": "Grand Palace & Wat Phra Kaew",
                            "description": "Visit Thailand's most sacred temple complex and former royal residence",
                            "location": "Na Phra Lan Rd, Phra Borom Maha Ratchawang",
                            "duration": "3 hours",
                            "cost": 500
                        },
                        {
                            "time": "12:30",
                            "activity": "Lunch at Thipsamai",
                            "description": "Famous for traditional Pad Thai",
                            "location": "313 Maha Chai Rd",
                            "duration": "1 hour",
                            "cost": 200
                        },
                        {
                            "time": "14:00",
                            "activity": "Wat Pho",
                            "description": "Temple of the Reclining Buddha",
                            "location": "2 Sanam Chai Rd",
                            "duration": "1.5 hours",
                            "cost": 200
                        },
                        {
                            "time": "16:00",
                            "activity": "Wat Arun",
                            "description": "Temple of Dawn across the river",
                            "location": "158 Thanon Wang Doem",
                            "duration": "1 hour",
                            "cost": 100
                        },
                        {
                            "time": "18:00",
                            "activity": "Dinner cruise on Chao Phraya River",
                            "description": "Enjoy Thai cuisine while seeing Bangkok from the water",
                            "location": "River City Pier",
                            "duration": "2 hours",
                            "cost": 1000
                        }
                    ]
                },
                {
                    "day": 2,
                    "title": "Modern Bangkok",
                    "activities": [
                        {
                            "time": "10:00",
                            "activity": "Shopping at Siam Paragon",
                            "description": "Upscale shopping mall",
                            "location": "Rama I Rd",
                            "duration": "2 hours",
                            "cost": 0
                        },
                        {
                            "time": "12:30",
                            "activity": "Lunch at Som Tam Nua",
                            "description": "Spicy Isaan food",
                            "location": "Siam Square Soi 5",
                            "duration": "1 hour",
                            "cost": 300
                        },
                        {
                            "time": "14:00",
                            "activity": "Jim Thompson House",
                            "description": "Traditional Thai house with art collection",
                            "location": "6 Soi Kasemsan 2",
                            "duration": "1.5 hours",
                            "cost": 200
                        },
                        {
                            "time": "16:00",
                            "activity": "MBK Center",
                            "description": "Shopping for electronics and souvenirs",
                            "location": "444 Phayathai Rd",
                            "duration": "2 hours",
                            "cost": 0
                        },
                        {
                            "time": "19:00",
                            "activity": "Dinner and drinks at Asiatique",
                            "description": "Riverside night market and entertainment venue",
                            "location": "2194 Charoen Krung Rd",
                            "duration": "3 hours",
                            "cost": 800
                        }
                    ]
                },
                {
                    "day": 3,
                    "title": "Local Experience",
                    "activities": [
                        {
                            "time": "08:00",
                            "activity": "Floating Market Tour",
                            "description": "Visit Damnoen Saduak floating market",
                            "location": "100 km southwest of Bangkok",
                            "duration": "5 hours",
                            "cost": 1000
                        },
                        {
                            "time": "14:00",
                            "activity": "Chatuchak Weekend Market",
                            "description": "Huge weekend market with everything imaginable",
                            "location": "Kamphaeng Phet 2 Rd",
                            "duration": "3 hours",
                            "cost": 0
                        },
                        {
                            "time": "18:00",
                            "activity": "Street food tour in Chinatown",
                            "description": "Sample the best of Thai street food",
                            "location": "Yaowarat Rd",
                            "duration": "2 hours",
                            "cost": 500
                        }
                    ]
                }
            ],
            "tags": ["temples", "shopping", "food", "cruise", "markets"],
            "created_at": datetime.datetime.now().isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Bangkok on a Budget - 4 Days",
            "description": "Explore Bangkok's highlights while keeping costs low",
            "duration": 4,
            "budget_category": "low",
            "budget_amount": 3000,
            "suitable_for": ["solo", "backpackers", "students"],
            "days": [
                {
                    "day": 1,
                    "title": "Temple Day",
                    "activities": [
                        {
                            "time": "09:00",
                            "activity": "Wat Pho",
                            "description": "Temple of the Reclining Buddha",
                            "location": "2 Sanam Chai Rd",
                            "duration": "1.5 hours",
                            "cost": 200
                        },
                        {
                            "time": "11:00",
                            "activity": "Lunch at local food stall",
                            "description": "Try local street food",
                            "location": "Around Wat Pho",
                            "duration": "1 hour",
                            "cost": 80
                        },
                        {
                            "time": "13:00",
                            "activity": "Wat Arun",
                            "description": "Temple of Dawn",
                            "location": "158 Thanon Wang Doem",
                            "duration": "1 hour",
                            "cost": 100
                        },
                        {
                            "time": "15:00",
                            "activity": "Free Museum Day",
                            "description": "National Museum (free on certain days)",
                            "location": "Na Phra That Rd",
                            "duration": "2 hours",
                            "cost": 0
                        },
                        {
                            "time": "18:00",
                            "activity": "Dinner at Or Tor Kor Market",
                            "description": "High-quality food market with reasonable prices",
                            "location": "Kamphaengphet Rd",
                            "duration": "1 hour",
                            "cost": 150
                        }
                    ]
                },
                {
                    "day": 2,
                    "title": "Local Markets",
                    "activities": [
                        {
                            "time": "08:00",
                            "activity": "Breakfast at hostel/hotel",
                            "description": "Save money by eating included breakfast",
                            "location": "Accommodation",
                            "duration": "30 mins",
                            "cost": 0
                        },
                        {
                            "time": "09:00",
                            "activity": "Chatuchak Weekend Market",
                            "description": "Huge weekend market",
                            "location": "Kamphaeng Phet 2 Rd",
                            "duration": "4 hours",
                            "cost": 0
                        },
                        {
                            "time": "13:00",
                            "activity": "Lunch at Chatuchak",
                            "description": "Food vendors in the market",
                            "location": "Chatuchak Market",
                            "duration": "1 hour",
                            "cost": 120
                        },
                        {
                            "time": "15:00",
                            "activity": "Free park visit",
                            "description": "Relax at Lumpini Park",
                            "location": "Rama IV Rd",
                            "duration": "2 hours",
                            "cost": 0
                        },
                        {
                            "time": "18:00",
                            "activity": "Street food dinner",
                            "description": "Try various street food options",
                            "location": "Victory Monument",
                            "duration": "1 hour",
                            "cost": 100
                        }
                    ]
                },
                {
                    "day": 3,
                    "title": "Cultural Day",
                    "activities": [
                        {
                            "time": "09:00",
                            "activity": "Free Art Gallery",
                            "description": "Bangkok Art and Culture Centre",
                            "location": "939 Rama I Rd",
                            "duration": "2 hours",
                            "cost": 0
                        },
                        {
                            "time": "12:00",
                            "activity": "Lunch at food court",
                            "description": "MBK Food Court - cheap and varied options",
                            "location": "MBK Center",
                            "duration": "1 hour",
                            "cost": 120
                        },
                        {
                            "time": "14:00",
                            "activity": "Walking tour of Chinatown",
                            "description": "Self-guided tour of Yaowarat",
                            "location": "Yaowarat Rd",
                            "duration": "3 hours",
                            "cost": 0
                        },
                        {
                            "time": "18:00",
                            "activity": "Chinatown street food",
                            "description": "Famous street food area",
                            "location": "Yaowarat Rd",
                            "duration": "2 hours",
                            "cost": 200
                        }
                    ]
                },
                {
                    "day": 4,
                    "title": "Off the Beaten Path",
                    "activities": [
                        {
                            "time": "07:00",
                            "activity": "Local breakfast",
                            "description": "Try Jok (rice porridge) at a local shop",
                            "location": "Local neighborhood",
                            "duration": "1 hour",
                            "cost": 60
                        },
                        {
                            "time": "08:30",
                            "activity": "Explore Thonburi",
                            "description": "Less visited side of the river",
                            "location": "Take the ferry across",
                            "duration": "3 hours",
                            "cost": 20
                        },
                        {
                            "time": "12:00",
                            "activity": "Lunch at local restaurant",
                            "description": "Non-touristy local food",
                            "location": "Thonburi area",
                            "duration": "1 hour",
                            "cost": 100
                        },
                        {
                            "time": "14:00",
                            "activity": "Visit Wat Pak Nam",
                            "description": "Less visited temple with beautiful murals",
                            "location": "Pak Nam",
                            "duration": "1.5 hours",
                            "cost": 0
                        },
                        {
                            "time": "17:00",
                            "activity": "Sunset at Golden Mount",
                            "description": "Panoramic views of Bangkok",
                            "location": "Wat Saket",
                            "duration": "1 hour",
                            "cost": 50
                        },
                        {
                            "time": "19:00",
                            "activity": "Farewell dinner at Raan Jay Fai",
                            "description": "Famous street food (splurge)",
                            "location": "327 Maha Chai Rd",
                            "duration": "2 hours",
                            "cost": 500
                        }
                    ]
                }
            ],
            "tags": ["budget", "temples", "markets", "street food", "local experience"],
            "created_at": datetime.datetime.now().isoformat()
        },
        {
            "id": str(uuid.uuid4()),
            "title": "Luxury Bangkok Experience - 2 Days",
            "description": "Experience Bangkok's finest luxury offerings",
            "duration": 2,
            "budget_category": "high",
            "budget_amount": 15000,
            "suitable_for": ["couples", "luxury travelers"],
            "days": [
                {
                    "day": 1,
                    "title": "Luxury Sightseeing",
                    "activities": [
                        {
                            "time": "08:00",
                            "activity": "Breakfast at hotel",
                            "description": "Gourmet breakfast at 5-star hotel",
                            "location": "Hotel restaurant",
                            "duration": "1 hour",
                            "cost": 800
                        },
                        {
                            "time": "09:30",
                            "activity": "Private Grand Palace Tour",
                            "description": "Private guided tour with expert historian",
                            "location": "Grand Palace",
                            "duration": "3 hours",
                            "cost": 3000
                        },
                        {
                            "time": "13:00",
                            "activity": "Lunch at Sala Rim Naam",
                            "description": "Fine Thai dining at Mandarin Oriental",
                            "location": "Mandarin Oriental Hotel",
                            "duration": "2 hours",
                            "cost": 2000
                        },
                        {
                            "time": "15:30",
                            "activity": "Thai spa treatment",
                            "description": "Premium spa package at Divana Spa",
                            "location": "Sukhumvit area",
                            "duration": "3 hours",
                            "cost": 3500
                        },
                        {
                            "time": "19:30",
                            "activity": "Rooftop dinner",
                            "description": "Fine dining at Sirocco or Vertigo",
                            "location": "State Tower or Banyan Tree",
                            "duration": "3 hours",
                            "cost": 4000
                        }
                    ]
                },
                {
                    "day": 2,
                    "title": "Exclusive Experiences",
                    "activities": [
                        {
                            "time": "09:00",
                            "activity": "Private longtail boat tour",
                            "description": "Explore Bangkok's canals in style",
                            "location": "Hotel pier",
                            "duration": "3 hours",
                            "cost": 2500
                        },
                        {
                            "time": "12:30",
                            "activity": "Lunch at Blue Elephant",
                            "description": "Royal Thai cuisine in colonial mansion",
                            "location": "233 Sathorn Tai Rd",
                            "duration": "2 hours",
                            "cost": 1800
                        },
                        {
                            "time": "15:00",
                            "activity": "Private shopping experience",
                            "description": "Personal shopping assistant at Emquartier",
                            "location": "Sukhumvit Rd",
                            "duration": "2 hours",
                            "cost": 0
                        },
                        {
                            "time": "18:00",
                            "activity": "Cocktails at Bamboo Bar",
                            "description": "Award-winning cocktails with live jazz",
                            "location": "Mandarin Oriental",
                            "duration": "1 hour",
                            "cost": 1000
                        },
                        {
                            "time": "20:00",
                            "activity": "Michelin-starred dinner",
                            "description": "Tasting menu at Gaggan Anand or Le Normandie",
                            "location": "Various locations",
                            "duration": "3 hours",
                            "cost": 5000
                        }
                    ]
                }
            ],
            "tags": ["luxury", "fine dining", "private tours", "spa", "rooftop"],
            "created_at": datetime.datetime.now().isoformat()
        }
    ]

def add_itineraries_to_collection(collection, itineraries):
    """Add itineraries to the ChromaDB collection"""
    # Check if collection already has documents
    if collection.count() > 0:
        print(f"Collection already has {collection.count()} documents. Skipping addition.")
        return
    
    ids = []
    documents = []
    metadatas = []
    
    for itinerary in itineraries:
        # Extract ID
        ids.append(itinerary["id"])
        
        # Create document for embedding (what will be used for similarity search)
        doc_text = f"{itinerary['title']} - {itinerary['description']} - "
        doc_text += f"Budget: {itinerary['budget_category']} ({itinerary['budget_amount']} THB) - "
        doc_text += f"Duration: {itinerary['duration']} days - "
        doc_text += f"Suitable for: {', '.join(itinerary['suitable_for'])} - "
        doc_text += f"Tags: {', '.join(itinerary['tags'])}"
        
        # Add activities summary
        for day in itinerary["days"]:
            doc_text += f" - Day {day['day']}: {day['title']} - "
            activities = [a["activity"] for a in day["activities"]]
            doc_text += ", ".join(activities)
        
        documents.append(doc_text)
        
        # Create metadata (will be returned with search results)
        metadatas.append({
            "title": itinerary["title"],
            "duration": itinerary["duration"],
            "budget_category": itinerary["budget_category"],
            "budget_amount": itinerary["budget_amount"],
            "suitable_for": ", ".join(itinerary["suitable_for"]),
            "tags": ", ".join(itinerary["tags"]),
            "full_data": json.dumps(itinerary)  # Store the full itinerary as JSON string
        })
    
    # Add to collection
    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )
    
    print(f"Added {len(ids)} itineraries to collection.")

def query_itineraries(query, budget=None, duration=None, traveler_type=None, n_results=3):
    """Query the itineraries collection based on user preferences"""
    client = get_chroma_client()
    try:
        collection = client.get_collection("bangkok_itineraries")
    except:
        # If collection doesn't exist, initialize and load data
        collection = initialize_itineraries_collection()
        itineraries = load_sample_itineraries()
        add_itineraries_to_collection(collection, itineraries)
        
    # Build the query string incorporating user preferences
    query_text = query
    if budget:
        query_text += f" with budget {budget}"
    if duration:
        query_text += f" for {duration} days"
    if traveler_type:
        query_text += f" suitable for {traveler_type}"
    
    # Query the collection
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    
    # Process results
    itineraries = []
    if results and len(results['metadatas']) > 0:
        for metadata in results['metadatas'][0]:
            # Convert the full_data JSON string back to dict
            if 'full_data' in metadata:
                itinerary = json.loads(metadata['full_data'])
                itineraries.append(itinerary)
    
    return itineraries

def format_itinerary_for_display(itinerary):
    """Format an itinerary for display in Streamlit"""
    markdown = f"## {itinerary['title']}\n\n"
    markdown += f"**Description:** {itinerary['description']}\n\n"
    markdown += f"**Duration:** {itinerary['duration']} days\n\n"
    markdown += f"**Budget Category:** {itinerary['budget_category'].capitalize()} (฿{itinerary['budget_amount']} THB)\n\n"
    markdown += f"**Suitable For:** {', '.join(itinerary['suitable_for'])}\n\n"
    markdown += f"**Tags:** {', '.join(itinerary['tags'])}\n\n"
    
    for day in itinerary['days']:
        markdown += f"### Day {day['day']}: {day['title']}\n\n"
        
        for activity in day['activities']:
            markdown += f"- **{activity['time']}** - **{activity['activity']}** (฿{activity['cost']} THB)\n"
            markdown += f"  *{activity['description']}* at {activity['location']} ({activity['duration']})\n\n"
    
    return markdown

def get_itinerary_html_card(itinerary):
    """Create HTML card for an itinerary suitable for display in the app"""
    total_cost = sum(sum(activity['cost'] for activity in day['activities']) for day in itinerary['days'])
    activity_count = sum(len(day['activities']) for day in itinerary['days'])
    
    html = f'''
    <div class="recommendation-card">
        <div class="card-title">{itinerary['title']}</div>
        <div class="card-meta">
            <span class="location-badge">📍 Bangkok</span>
            <span class="type-badge">{itinerary['duration']} Days</span>
        </div>
        <p>{itinerary['description']}<br>
        <small>{activity_count} activities • Suitable for {', '.join(itinerary['suitable_for'])}</small></p>
        <div class="card-footer">
            <span class="price-tag">฿{total_cost} THB</span>
            <span class="rating">{'🏷️ ' + ', '.join(itinerary['tags'][:3])}</span>
        </div>
    </div>
    '''
    return html

def initialize_db():
    """Initialize the ChromaDB database with sample itineraries"""
    collection = initialize_itineraries_collection()
    itineraries = load_sample_itineraries()
    add_itineraries_to_collection(collection, itineraries)
    return collection
def query_similar_itineraries(query_text, collection_name="bangkok_itineraries", top_k=3):
    """Query ChromaDB for similar itineraries"""
    client = get_chroma_client()
    collection = client.get_collection(collection_name)

    results = collection.query(
        query_texts=[query_text],
        n_results=top_k
    )

    # Process results
    itineraries = []
    if results and len(results['metadatas']) > 0:
        for metadata in results['metadatas'][0]:
            if 'full_data' in metadata:
                itinerary = json.loads(metadata['full_data'])
                itineraries.append(itinerary)

    return itineraries
