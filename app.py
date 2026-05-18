import streamlit as st
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import random

# Initialize Geolocator (Uses OpenStreetMap/Google equivalent open-source API)
geolocator = Nominatim(user_agent="india_map_educational_app_v2")

# Structure Map Data extracted directly from the Class X Map Work PDF
MAP_DATA = {
    "Iron Ore Mines": [
        {"name": "Mayurbhanj", "state": "Odisha"},
        {"name": "Durg", "state": "Chhattisgarh"},
        {"name": "Bailadila", "state": "Chhattisgarh"},
        {"name": "Bellary", "state": "Karnataka"},
        {"name": "Kudremukh", "state": "Karnataka"}
    ],
    "Oil Fields": [
        {"name": "Digboi", "state": "Assam"},
        {"name": "Naharkatia", "state": "Assam"},
        {"name": "Mumbai High", "state": "Arabian Sea"},
        {"name": "Bassein", "state": "Arabian Sea"},
        {"name": "Kalol", "state": "Gujarat"},
        {"name": "Ankleshwar", "state": "Gujarat"}
    ],
    "Dams": [
        {"name": "Salal", "state": "Jammu & Kashmir"},
        {"name": "Bhakra Nangal", "state": "Himachal Pradesh"},
        {"name": "Tehri", "state": "Uttarakhand"},
        {"name": "Rana Pratap Sagar", "state": "Rajasthan"},
        {"name": "Sardar Sarovar", "state": "Gujarat"},
        {"name": "Hirakud", "state": "Odisha"},
        {"name": "Nagarjuna Sagar", "state": "Telangana"},
        {"name": "Tungbhadra", "state": "Karnataka"}
    ],
    "Centres of Indian National Movement": [
        {"name": "Champaran", "state": "Bihar"},
        {"name": "Kheda", "state": "Gujarat"},
        {"name": "Ahmedabad", "state": "Gujarat"},
        {"name": "Chauri Chaura", "state": "Uttar Pradesh"},
        {"name": "Amritsar", "state": "Punjab"},
        {"name": "Dandi", "state": "Gujarat"}
    ],
    "Congress Sessions": [
        {"name": "Calcutta (Sept. 1920)", "state": "West Bengal"},
        {"name": "Nagpur (Dec. 1920)", "state": "Maharashtra"},
        {"name": "Madras (1927)", "state": "Tamil Nadu"}
    ],
    "Nuclear Power Plants": [
        {"name": "Narora", "state": "Uttar Pradesh"},
        {"name": "Kakrapar", "state": "Gujarat"},
        {"name": "Tarapur", "state": "Maharashtra"},
        {"name": "Kalpakkam", "state": "Tamil Nadu"}
    ],
    "Thermal Power Plants": [
        {"name": "Namrup", "state": "Assam"},
        {"name": "Singrauli", "state": "Madhya Pradesh"},
        {"name": "Ramagundam", "state": "Telangana"}
    ],
    "Iron and Steel Plants": [
        {"name": "Durgapur", "state": "West Bengal"},
        {"name": "Bokaro", "state": "Jharkhand"},
        {"name": "Jamshedpur", "state": "Jharkhand"},
        {"name": "Bhilai", "state": "Chhattisgarh"},
        {"name": "Vijayanagar", "state": "Karnataka"},
        {"name": "Salem", "state": "Tamil Nadu"}
    ],
    "Major Ports": [
        {"name": "Kandla", "state": "Gujarat"},
        {"name": "Mumbai", "state": "Maharashtra"},
        {"name": "Marmagao", "state": "Goa"},
        {"name": "New Mangalore", "state": "Karnataka"},
        {"name": "Kochi", "state": "Kerala"},
        {"name": "Tuticorin", "state": "Tamil Nadu"},
        {"name": "Chennai", "state": "Tamil Nadu"},
        {"name": "Vishakhapatnam", "state": "Andhra Pradesh"},
        {"name": "Paradip", "state": "Odisha"},
        {"name": "Haldia", "state": "West Bengal"}
    ],
    "International Airports": [
        {"name": "Amritsar (Raja Sansi)", "state": "Punjab"},
        {"name": "Delhi (Indira Gandhi International)", "state": "Delhi"},
        {"name": "Mumbai (Chhatrapati Shivaji)", "state": "Maharashtra"},
        {"name": "Chennai (Meenambakkam)", "state": "Tamil Nadu"},
        {"name": "Kolkata (Netaji Subhash Chandra Bose)", "state": "West Bengal"},
        {"name": "Hyderabad (Rajiv Gandhi)", "state": "Telangana"}
    ]
}

# Geocoding logic to auto-adopt geographical positions
@st.cache_data
def get_coordinates(name, state):
    try:
        # Clean up airport names for cleaner map search matching
        search_name = name.split("(")[0].strip()
        query = f"{search_name}, {state}, India" if "Arabian Sea" not in state else f"{search_name}, Arabian Sea"
        location = geolocator.geocode(query, timeout=10)
        if location:
            return [location.latitude, location.longitude]
    except Exception:
        pass
    
    # Accurate fallback dataset values if API limits apply or connection times out
    fallbacks = {
        "Mumbai High": [19.4192, 71.3831], "Bassein": [19.3304, 72.8101],
        "Bailadila": [18.6214, 81.2494], "Kudremukh": [13.2181, 75.2479],
        "Chauri Chaura": [26.6438, 83.5883], "Champaran": [26.8459, 84.5161]
    }
    return fallbacks.get(name, [20.5937, 78.9629])

# --- Streamlit Page Setup ---
st.set_page_config(page_title="Class X Map Station", layout="wide")
st.title("🗺️ CBSE Class 10 Interactive Map practice Work")
st.write("Automatically loads map positions from the syllabus. Check the layout map or test your knowledge in the practice sets below.")

tabs = st.tabs(["Interactive Map Viewer", "Student Practice & Test Set"])

# --- TAB 1: INTERACTIVE VIEW ---
with tabs[0]:
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("Configuration Panel")
        category = st.selectbox("Choose Map Category", list(MAP_DATA.keys()))
        
        places_in_cat = [item["name"] for item in MAP_DATA[category]]
        selected_places = st.multiselect("Select Places to Display", places_in_cat, default=places_in_cat)
        
        map_style = st.selectbox("Base Layout Design", ["OpenStreetMap", "CartoDB positron", "CartoDB dark_matter"])

    with col2:
        m = folium.Map(location=[22.0, 78.9], zoom_start=5, tiles=map_style)
        
        for item in MAP_DATA[category]:
            if item["name"] in selected_places:
                coords = get_coordinates(item["name"], item["state"])
                folium.Marker(
                    location=coords,
                    popup=folium.Popup(f"<b>{item['name']}</b><br>State: {item['state']}<br>Syllabus: {category}", max_width=250),
                    tooltip=item["name"],
                    icon=folium.Icon(color="blue", icon="geo-alt-fill", prefix="fa")
                ).add_to(m)
        
        st_folium(m, width="100%", height=550)

# --- TAB 2: EXAM PRACTICE SET ---
with tabs[1]:
    st.subheader("📝 Class X Board Self-Practice Exam Station")
    st.write("Test your knowledge identifying locations accurately for board examinations.")
    
    if "quiz_data" not in st.session_state:
        all_items = [(cat, item) for cat, items in MAP_DATA.items() for item in items]
        st.session_state.quiz_data = random.sample(all_items, min(5, len(all_items)))
        st.session_state.answers = {}
        st.session_state.submitted = False

    if st.button("🔄 Load a New Random Test Set"):
        all_items = [(cat, item) for cat, items in MAP_DATA.items() for item in items]
        st.session_state.quiz_data = random.sample(all_items, 5)
        st.session_state.answers = {}
        st.session_state.submitted = False
        st.rerun()

    for idx, (cat, item) in enumerate(st.session_state.quiz_data):
        clean_cat = cat[:-1] if cat.endswith("s") else cat
        st.markdown(f"**Question {idx+1}:** Where is the **{clean_cat}** named **'{item['name']}'** located?")
        
        wrong_states = list(set([i["state"] for c, items in MAP_DATA.items() for i in items if i["state"] != item["state"]]))
        options = list(set([item["state"]] + random.sample(wrong_states, min(3, len(wrong_states)))))
        random.shuffle(options)
        
        st.session_state.answers[idx] = st.radio(
            f"Select correct state territory location for {item['name']}:", 
            options, 
            key=f"q_{idx}",
            index=None
        )
        st.divider()

    if st.button("📤 Submit Final Test Answers"):
        st.session_state.submitted = True
        score = 0
        for idx, (cat, item) in enumerate(st.session_state.quiz_data):
            user_ans = st.session_state.answers.get(idx)
            correct_ans = item["state"]
            if user_ans == correct_ans:
                score += 1
                st.success(f"✔️ Question {idx+1}: Correct! **{item['name']}** is located in **{correct_ans}**.")
            else:
                st.error(f"❌ Question {idx+1}: Incorrect. **{item['name']}** is in **{correct_ans}** (You picked: {user_ans}).")
        
        st.metric(label="Your Evaluation Score", value=f"{score} / 5")
