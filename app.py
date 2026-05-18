import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import random

# Initialize Geolocator
geolocator = Nominatim(user_agent="cbse_class10_final_board_prep_2026")

# Comprehensive CBSE Class X Map Work Dataset
MAP_DATA = {
    # --- HISTORY: Nationalism in India ---
    "History: Congress Sessions": [
        {"name": "Calcutta (Sept. 1920)", "state": "West Bengal"},
        {"name": "Nagpur (Dec. 1920)", "state": "Maharashtra"},
        {"name": "Madras (1927)", "state": "Tamil Nadu"}
    ],
    "History: Freedom Movement Important Centres": [
        {"name": "Champaran (Indigo Planters)", "state": "Bihar"},
        {"name": "Kheda (Peasant Satyagraha)", "state": "Gujarat"},
        {"name": "Ahmedabad (Cotton Mill Workers)", "state": "Gujarat"},
        {"name": "Jallianwala Bagh (Amritsar)", "state": "Punjab"},
        {"name": "Dandi (Civil Disobedience)", "state": "Gujarat"}
    ],
    
    # --- GEOGRAPHY: Water Resources ---
    "Geography: Important Dams": [
        {"name": "Salal", "state": "Jammu & Kashmir"},
        {"name": "Bhakra Nangal", "state": "Himachal Pradesh"},
        {"name": "Tehri", "state": "Uttarakhand"},
        {"name": "Rana Pratap Sagar", "state": "Rajasthan"},
        {"name": "Sardar Sarovar", "state": "Gujarat"},
        {"name": "Hirakud", "state": "Odisha"},
        {"name": "Nagarjuna Sagar", "state": "Telangana"},
        {"name": "Tungbhadra", "state": "Karnataka"}
    ],
    
    # --- GEOGRAPHY: Minerals and Energy Resources ---
    "Geography: Iron Ore Mines": [
        {"name": "Mayurbhanj", "state": "Odisha"},
        {"name": "Durg", "state": "Chhattisgarh"},
        {"name": "Bailadila", "state": "Chhattisgarh"},
        {"name": "Bellary", "state": "Karnataka"},
        {"name": "Kudremukh", "state": "Karnataka"}
    ],
    "Geography: Coal Mines": [
        {"name": "Raniganj", "state": "West Bengal"},
        {"name": "Bokaro (Coal Mine)", "state": "Jharkhand"},
        {"name": "Talcher", "state": "Odisha"},
        {"name": "Neyveli", "state": "Tamil Nadu"}
    ],
    "Geography: Oil Fields": [
        {"name": "Digboi", "state": "Assam"},
        {"name": "Naharkatia", "state": "Assam"},
        {"name": "Mumbai High", "state": "Arabian Sea"},
        {"name": "Bassein", "state": "Arabian Sea"},
        {"name": "Kalol", "state": "Gujarat"},
        {"name": "Ankleshwar", "state": "Gujarat"}
    ],
    "Geography: Thermal Power Plants": [
        {"name": "Namrup", "state": "Assam"},
        {"name": "Singrauli", "state": "Madhya Pradesh"},
        {"name": "Ramagundam", "state": "Telangana"}
    ],
    "Geography: Nuclear Power Plants": [
        {"name": "Narora", "state": "Uttar Pradesh"},
        {"name": "Kakrapar", "state": "Gujarat"},
        {"name": "Tarapur", "state": "Maharashtra"},
        {"name": "Kalpakkam", "state": "Tamil Nadu"}
    ],
    
    # --- GEOGRAPHY: Manufacturing Industries ---
    "Geography: Cotton Textile Industries": [
        {"name": "Mumbai (Cotton Textile)", "state": "Maharashtra"},
        {"name": "Indore", "state": "Madhya Pradesh"},
        {"name": "Surat", "state": "Gujarat"},
        {"name": "Kanpur", "state": "Uttar Pradesh"},
        {"name": "Coimbatore", "state": "Tamil Nadu"}
    ],
    "Geography: Iron and Steel Plants": [
        {"name": "Durgapur", "state": "West Bengal"},
        {"name": "Bokaro (Iron & Steel)", "state": "Jharkhand"},
        {"name": "Jamshedpur", "state": "Jharkhand"},
        {"name": "Bhilai", "state": "Chhattisgarh"},
        {"name": "Vijayanagar", "state": "Karnataka"},
        {"name": "Salem", "state": "Tamil Nadu"}
    ],
    "Geography: Software Technology Parks": [
        {"name": "Noida", "state": "Uttar Pradesh"},
        {"name": "Gandhinagar", "state": "Gujarat"},
        {"name": "Mumbai (STP)", "state": "Maharashtra"},
        {"name": "Pune", "state": "Maharashtra"},
        {"name": "Hyderabad", "state": "Telangana"},
        {"name": "Bengaluru", "state": "Karnataka"},
        {"name": "Chennai (STP)", "state": "Tamil Nadu"},
        {"name": "Thiruvananthapuram", "state": "Kerala"}
    ],
    
    # --- GEOGRAPHY: Lifelines of National Economy ---
    "Geography: Major Sea Ports": [
        {"name": "Kandla", "state": "Gujarat"},
        {"name": "Mumbai (Port)", "state": "Maharashtra"},
        {"name": "Marmagao", "state": "Goa"},
        {"name": "New Mangalore", "state": "Karnataka"},
        {"name": "Kochi", "state": "Kerala"},
        {"name": "Tuticorin", "state": "Tamil Nadu"},
        {"name": "Chennai (Port)", "state": "Tamil Nadu"},
        {"name": "Vishakhapatnam", "state": "Andhra Pradesh"},
        {"name": "Paradip", "state": "Odisha"},
        {"name": "Haldia", "state": "West Bengal"}
    ],
    "Geography: International Airports": [
        {"name": "Amritsar (Raja Sansi - Sri Guru Ram Das ji)", "state": "Punjab"},
        {"name": "Delhi (Indira Gandhi)", "state": "Delhi"},
        {"name": "Mumbai (Chhatrapati Shivaji)", "state": "Maharashtra"},
        {"name": "Chennai (Meenambakkam)", "state": "Tamil Nadu"},
        {"name": "Kolkata (Netaji Subhash Chandra Bose)", "state": "West Bengal"},
        {"name": "Hyderabad (Rajiv Gandhi)", "state": "Telangana"}
    ]
}

# Geocoding function logic with customized search handling
@st.cache_data
def get_coordinates(name, state):
    try:
        clean_name = name.split("(")[0].strip()
        query = f"{clean_name}, {state}, India" if "Arabian Sea" not in state else f"{clean_name}, Arabian Sea"
        location = geolocator.geocode(query, timeout=10)
        if location:
            return [location.latitude, location.longitude]
    except Exception:
        pass
    
    fallbacks = {
        "Mumbai High": [19.4192, 71.3831], "Bassein": [19.3304, 72.8101],
        "Bailadila": [18.6214, 81.2494], "Kudremukh": [13.2181, 75.2479],
        "Chauri Chaura": [26.6438, 83.5883], "Champaran (Indigo Planters)": [26.8459, 84.5161],
        "Amritsar (Raja Sansi - Sri Guru Ram Das ji)": [31.7096, 74.8002],
        "Kakrapra": [21.2655, 73.3512], "Kakrapara": [21.2655, 73.3512],
        "Neyveli": [11.5367, 79.4820], "Talcher": [20.9520, 85.2282]
    }
    return fallbacks.get(name, [22.0, 78.9])

# --- Streamlit Layout Customization ---
st.set_page_config(page_title="CBSE Class 10 Map Prep Terminal", layout="wide")

# Injection of UI/UX Branding Elements matching Portal Core Hub Themes
st.markdown("""
    <style>
    /* Main Background Theme Setup */
    .stApp {
        background: linear-gradient(180deg, #0b5ea8 0%, #314755 55%, #26a0da 100%) !important;
        color: #ffffff !important;
    }
    
    /* Unified Header Custom Container */
    .branding-container {
        display: flex;
        align-items: center;
        gap: 20px;
        padding: 15px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        margin-bottom: 25px;
    }
    .brand-logo {
        height: 85px;
        object-fit: contain;
    }
    .brand-text-block {
        display: flex;
        flex-direction: column;
    }
    .main-academy-title {
        font-size: 38px;
        font-weight: 800;
        color: #FFD700;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.4);
        font-family: sans-serif;
    }
    .sub-academy-title {
        font-size: 20px;
        font-weight: 600;
        color: #ffffff;
        margin: 0;
    }
    
    /* Force text elements to always remain visible white */
    h1, h2, h3, h4, h5, h6, label, p, .stWidgetLabel, div, span {
        color: #ffffff !important;
    }
    
    /* ==========================================================================
       CRITICAL FIX: SELECT BOX / MULTISELECT DROPDOWN VISIBILITY FIX
       ========================================================================== */
    /* Target select box input fields container */
    div[data-baseweb="select"] div {
        color: #FFD700 !important; /* Force visible black/dark text inside active selectors */
        background-color: #ffffff !important;
    }
    
    /* Target the dropdown overlay popover list items */
    ul[role="listbox"] li, ul[role="listbox"] div {
        color: #000000 !important; /* Make options inside dropdown list completely dark and viewable */
        background-color: #ffffff !important;
    }
    ul[role="listbox"] li:hover {
        background-color: #ffffff !important; /* light blue highlight on hovering selections */
    }

    /* Target chosen pills/chips inside multiselect containers */
    div[data-testid="stMultiSelectFloatingValue"] span, div[role="button"] span {
        color: #000000 !important;
    }
    
    /* Custom Styling for Streamlit Buttons */
    div.stButton > button {
        background: linear-gradient(to right, #314755 0%, #26a0da 51%, #314755 100%) !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 12px 28px !important;
        font-size: 16px !important;
        font-weight: bold !important;
        text-transform: uppercase !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
        transition: 0.5s !important;
        background-size: 200% auto !important;
        width: 100%;
    }
    div.stButton > button:hover {
        background-position: right center !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.4) !important;
    }
    
    /* Clean Cards for Dropdown Selectors & Modules */
    div[data-testid="stBlock"] {
        background: rgba(255, 255, 255, 0.08) !important;
        padding: 20px !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Tab Styling Overrides */
    button[data-baseweb="tab"] {
        color: #ffffff !important;
        font-weight: bold !important;
        font-size: 16px !important;
    }
    button[aria-selected="true"] {
        color: #FFD700 !important;
        border-bottom-color: #FFD700 !important;
    }
    
    /* Metric / Evaluation Score Box styles */
    div[data-testid="stMetricValue"] {
        color: #FFD700 !important;
        font-size: 42px !important;
        font-weight: 800 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Custom Header Wrapper Injection with Image Logo Array
LOGO_URL = "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiQ6lxEfFnImeGWEf7I7Fg9z-uCCkAdKWwxtHLn4zzcyCElV3DupEdwzEKpBin5ucTMpCLDbgwqN_cUkj7qhXDdgAIAvIFLdSJfl2byeN8e4_4oaVImEQQB9lYD-5qrC0mDqWWdXEFuhXy6jViTvcc-6LB6sJa3a2okWqasLjDKMoOxcbvtlUwCLxP5JEl6/s320/Gemini_Generated_Image_ce701rce701rce70-removebg-preview.png"

st.markdown(f"""
    <div class="branding-container">
        <img class="brand-logo" src="{LOGO_URL}" alt="MY SST ACADEMY LOGO">
        <div class="brand-text-block">
            <h1 class="main-academy-title">MY SST ACADEMY</h1>
            <h2 class="sub-academy-title">🎯 CBSE Class X Map Works as per Academic Session: 2026-27</h2>
        </div>
    </div>
""", unsafe_allow_html=True)

st.write("Master your full 5 Marks syllabus items dynamically via outline map visualization or endless evaluation testing cycles.")

tabs = st.tabs(["👁️ Interactive Map Viewer", "📝 Infinite Practice Sets"])

# --- TAB 1: SYLLABUS LAYOUT VIEWER ---
with tabs[0]:
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("Syllabus Engine Layout")
        category = st.selectbox("Choose Textbook Map Topic", list(MAP_DATA.keys()))
        
        places_in_cat = [item["name"] for item in MAP_DATA[category]]
        selected_places = st.multiselect("Toggle Specific Locations", places_in_cat, default=places_in_cat)
        map_style = st.selectbox("Outline Map Display Texture", ["CartoDB positron", "OpenStreetMap", "CartoDB dark_matter"])
        
        st.info("💡 Pro-Tip: Select 'CartoDB positron'. It strips away details, leaving a clean outline template matching your actual Board examination papers.")

    with col2:
        m = folium.Map(location=[22.0, 78.9], zoom_start=5, tiles=map_style)
        
        for item in MAP_DATA[category]:
            if item["name"] in selected_places:
                coords = get_coordinates(item["name"], item["state"])
                folium.Marker(
                    location=coords,
                    popup=folium.Popup(f"<b>{item['name']}</b><br>State Location: {item['state']}<br>Syllabus Division: {category}", max_width=250),
                    tooltip=item["name"],
                    icon=folium.Icon(color="red" if "History" in category else "blue", icon="info-sign")
                ).add_to(m)
        
        st_folium(m, width="100%", height=600)

# --- TAB 2: INFINITE PRACTICE ROOM ---
with tabs[1]:
    st.subheader("🧠 Unlimited Self-Assessment Test")
    st.write("Practise an infinite variety of combinations. Questions mirror identification styles seen in the board exam.")
    
    if "quiz_data" not in st.session_state:
        all_items = [(cat, item) for cat, items in MAP_DATA.items() for item in items]
        st.session_state.quiz_data = random.sample(all_items, min(5, len(all_items)))
        st.session_state.answers = {}
        st.session_state.submitted = False

    if st.button("🔄 New Mock Test Set"):
        all_items = [(cat, item) for cat, items in MAP_DATA.items() for item in items]
        st.session_state.quiz_data = random.sample(all_items, 5)
        st.session_state.answers = {}
        st.session_state.submitted = False
        st.rerun()

    for idx, (cat, item) in enumerate(st.session_state.quiz_data):
        st.markdown(f"**Question {idx+1}:** Identify the correct State/Territory where the listed feature **'{item['name']}'** (From *{cat}*) is located:")
        
        wrong_states = list(set([i["state"] for c, items in MAP_DATA.items() for i in items if i["state"] != item["state"]]))
        options = list(set([item["state"]] + random.sample(wrong_states, min(3, len(wrong_states)))))
        random.shuffle(options)
        
        st.session_state.answers[idx] = st.radio(
            f"Select positioning boundary for {item['name']}:", 
            options, 
            key=f"q_{idx}",
            index=None
        )
        st.divider()

    if st.button("📤 Submit Final Answer Sheet"):
        st.session_state.submitted = True
        score = 0
        for idx, (cat, item) in enumerate(st.session_state.quiz_data):
            user_ans = st.session_state.answers.get(idx)
            correct_ans = item["state"]
            if user_ans == correct_ans:
                score += 1
                st.success(f"✔️ Question {idx+1}: Correct! **{item['name']}** belongs within **{correct_ans}**.")
            else:
                st.error(f"❌ Question {idx+1}: Wrong Choice. **{item['name']}** is located within **{correct_ans}** (You selected: {user_ans}).")
        
        st.metric(label="Your Mock Evaluation Score", value=f"{score} / 5")
