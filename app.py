import streamlit as st
import folium
from streamlit_folium import st_folium
import random
import streamlit.components.v1 as components

# --- HYPER-EXACT CBSE MAP COORDINATES DATASET (2026 UPDATED) ---
COORDINATE_LOOKUP = {
    # --- History: National Movement ---
    "Calcutta (Sept. 1920)": [22.5645, 88.3520],       # Wellington Square / Subodh Mallick Square area (historic meet site)
    "Nagpur (Dec. 1920)": [21.1443, 79.0849],         # Historic town hall / central congregation area
    "Madras (1927)": [13.0604, 80.2496],              # Spur Tank road area (historic Congress session grounds)
    "Champaran (Indigo Planters)": [26.8449, 84.5042], # Core historic district area of Motihari, Champaran
    "Kheda (Peasant Satyagraha)": [22.7519, 72.6858],  # Nadiad/Kheda core movement area
    "Ahmedabad (Cotton Mill Workers)": [23.0242, 72.5890], # Sabarmati Old Mill area
    "Jallianwala Bagh (Amritsar)": [31.6366, 74.8762], # Exactly on the Jallianwala Bagh Martyr's Memorial
    "Dandi (Civil Disobedience)": [20.8916, 72.7932],  # Exactly on the National Salt Satyagraha Memorial

    # --- Geography: Dams & Water Resources ---
    "Salal": [33.1477, 74.8058],                       # Center of the Salal Dam concrete spillway
    "Bhakra Nangal": [31.4081, 76.4347],               # Exactly on the Bhakra Dam structure over Sutlej
    "Tehri": [30.3794, 78.4793],                       # Exactly on the Tehri Dam embankment wall
    "Rana Pratap Sagar": [24.9231, 75.5801],           # Exactly on the Rana Pratap Sagar Dam wall
    "Sardar Sarovar": [21.8310, 73.7484],              # Exactly on the main concrete gravity dam wall
    "Hirakud": [21.5284, 83.8711],                     # Center of the main concrete dam section
    "Nagarjuna Sagar": [16.5755, 79.3116],             # Exactly on the center of the masonry dam wall
    "Tungbhadra": [15.2574, 76.3408],                  # Center of the Tungabhadra Dam crest gates

    # --- Geography: Iron Ore Mines ---
    "Mayurbhanj": [22.1812, 86.2223],                  # Gorumahisani Iron Ore Mine complex
    "Durg": [20.6122, 81.1895],                        # Rajhara Iron Ore Mine pit area (Durg/Balod range)
    "Bailadila": [18.6500, 81.2200],                   # Center of the active open-cast mining ridge
    "Bellary": [15.1512, 76.6614],                     # Sandur iron ore belt mining zone near Bellary
    "Kudremukh": [13.2642, 75.2476],                   # Old KIOCL mining/crushing plant facility

    # --- Geography: Coal Mines ---
    "Raniganj": [23.6190, 87.1084],                    # Core Raniganj coalfield operational area
    "Bokaro (Coal Mine)": [23.7744, 85.8712],           # Active coal extraction pit, Bokaro fields
    "Talcher": [20.9575, 85.1784],                     # Core MCL open-cast coal mining zone
    "Neyveli": [11.5332, 79.4316],                     # Mine-1 open cast lignite excavation pit

    # --- Geography: Oil Fields ---
    "Digboi": [27.3811, 95.6375],                      # Historic Digboi Well No. 1 and Refinery hub
    "Naharkatia": [27.2912, 95.3411],                  # Core oil-producing extraction cluster
    "Mumbai High": [19.4192, 71.3831],                 # Actual offshore marine platform coordinates
    "Bassein": [19.3101, 72.1124],                     # Offshore Vasai/Bassein gas field platform area
    "Kalol": [23.2514, 72.4988],                       # ONGC active oil production facility
    "Ankleshwar": [21.6114, 73.0182],                  # ONGC central oil extraction hub

    # --- Geography: Power Plants (Thermal & Nuclear) ---
    "Namrup": [27.1866, 95.3892],                      # Namrup Thermal Power Station complex
    "Singrauli": [24.2012, 82.7052],                   # NTPC Singrauli Super Thermal Power Plant units
    "Ramagundam": [18.7562, 79.4511],                  # NTPC Ramagundam Power Plant footprint
    "Narora": [28.1554, 78.4116],                      # Narora Atomic Power Station reactor domes
    "Kakrapar": [21.2386, 73.3486],                    # Kakrapar Atomic Power Station facility
    "Tarapur": [19.8392, 72.7464],                     # Tarapur Atomic Power Station core reactors
    "Kalpakkam": [12.5574, 80.1581],                   # Madras Atomic Power Station (Kalpakkam)

    # --- Geography: Cotton Textile Industries ---
    "Mumbai (Cotton Textile)": [18.9912, 72.8310],     # Girangaon (historic Mill lands district of Mumbai)
    "Indore": [22.7275, 75.8642],                      # Historic Malwa Mills textile industrial area
    "Surat": [21.2012, 72.8414],                       # Core textile manufacturing/industrial zone
    "Kanpur": [26.4714, 80.3521],                      # Elgin/Muir Mills historic textile area near river
    "Coimbatore": [11.0124, 76.9692],                  # Core textile mill cluster area

    # --- Geography: Iron & Steel Plants ---
    "Durgapur": [23.5518, 87.2798],                    # Durgapur Steel Plant (SAIL) main blast furnaces
    "Bokaro (Iron & Steel)": [23.6675, 86.0911],       # Bokaro Steel Plant (SAIL) core manufacturing complex
    "Jamshedpur": [22.7801, 86.1952],                  # Tata Steel Works main factory footprint
    "Bhilai": [21.1764, 81.3912],                      # Bhilai Steel Plant (SAIL) operations plant
    "Vijayanagar": [15.1911, 76.6714],                 # JSW Steel Vijayanagar works industrial campus
    "Salem": [11.6441, 78.0298],                       # Salem Steel Plant (SAIL) processing complex

    # --- Geography: Software Technology Parks (STPI) ---
    "Noida": [28.5911, 77.3114],                       # Sector 62 / Sector 63 IT & STPI hub
    "Gandhinagar": [23.2198, 72.6842],                 # Infocity / Gift City IT park zone
    "Mumbai (STP)": [19.1172, 72.8824],                # Seepz (Santacruz Electronic Export Processing Zone)
    "Pune": [18.5914, 73.7412],                        # Hinjawadi Rajiv Gandhi Infotech Park Phase 1
    "Hyderabad": [17.4436, 78.3742],                   # HITEC City / Cyberabad tech hub
    "Bengaluru": [12.9864, 77.7314],                   # International Tech Park Bangalore (ITPB), Whitefield
    "Chennai (STP)": [12.9642, 80.2458],               # Taramani Rajiv Gandhi Salai (OMR) IT Corridor
    "Thiruvananthapuram": [8.5524, 76.8796],           # Technopark Campus Phase 1

    # --- Geography: Major Sea Ports ---
    "Kandla": [23.0014, 70.2241],                      # Deendayal Port (Kandla) main cargo berths
    "Mumbai (Port)": [18.9484, 72.8514],               # Mumbai Port Trust docking berths
    "Marmagao": [15.4112, 73.8114],                    # Marmagao Port iron ore handling berths
    "New Mangalore": [12.9284, 74.8198],               # New Mangalore Port entry channels
    "Kochi": [9.9642, 76.2614],                        # Willingdon Island / Vallarpadam Terminal berths
    "Tuticorin": [8.7511, 78.1642],                    # VOC Port Tuticorin shipping docks
    "Chennai (Port)": [13.0924, 80.2974],              # Chennai Port Trust main harbor container terminal
    "Vishakhapatnam": [17.6812, 83.2942],              # Vizag Port inner harbor docking channel
    "Paradip": [20.2611, 86.6714],                     # Paradip Port mechanized cargo berths
    "Haldia": [22.0212, 88.0614],                      # Haldia Dock Complex (HDC) berths

    # --- Geography: International Airports ---
    "Amritsar (Raja Sansi - Sri Guru Ram Das ji)": [31.7081, 74.8014], # Main Terminal building
    "Delhi (Indira Gandhi)": [28.5572, 77.0911],                       # Exactly on Terminal 3 building
    "Mumbai (Chhatrapati Shivaji)": [19.0901, 72.8628],                # Exactly on Terminal 2 integrated wing
    "Chennai (Meenambakkam)": [12.9914, 80.1742],                      # International/Domestic passenger terminal
    "Kolkata (Netaji Subhash Chandra Bose)": [22.6520, 88.4462],       # Integrated Terminal building canopy
    "Hyderabad (Rajiv Gandhi)": [17.2414, 78.4298]                     # Shamshabad Main Passenger Terminal
}


MAP_DATA = {
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

@st.cache_data
def get_coordinates(name, state):
    return COORDINATE_LOOKUP.get(name, [22.0, 78.9])

st.set_page_config(page_title="CBSE Class 10 Map Prep Terminal", layout="wide")

st.markdown("""
<style>
    .stApp {
      background: linear-gradient(180deg, #0b5ea8 0%, #314755 55%, #26a0da 100%) !important; 
        color: #ffffff !important;
    }
    .branding-container {
        display: flex;
        align-items: center;
        gap: 10px;
       padding: 2px 8px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        margin-bottom: 15px;
    }
    .brand-logo {
        height: 100px;
        object-fit: contain;
    }
    .brand-text-block {
    display: flex;
    flex-direction: column;
    gap: 1px;
    line-height: 1.1;
    }
    .main-academy-title {
        font-size: 60px;
        font-weight: 800;
        color: #FFD700;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.4);
        font-family: sans-serif;
    }
    .sub-academy-title {
        font-size: 15px;
        font-weight: 600;
        color: #ffffff;
        margin: 0;
    }
        
    h1, h2, h3, h4, h5, h6, label, .stWidgetLabel {
        color: #ffffff !important;
    }
    div[data-testid="stMarkdownContainer"] p {
        color: #ffffff !important;
    }
    label[data-testid="stWidgetLabel"] p {
        color: #ffffff !important;
        font-weight: 600 !important;
    }

    div[data-baseweb="select"] > div {
        background-color: #1a2d3b !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
    }
    div[data-baseweb="select"] [data-testid="stMarkdownContainer"] p,
    div[data-baseweb="select"] svg,
    div[data-baseweb="select"] div {
        color: #ffffff !important;
        fill: #ffffff !important;
    }
        
    div[data-baseweb="popover"], 
    div[role="listbox"], 
    ul[role="listbox"] {
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    div[role="option"], 
    div[role="option"] span,
    ul[role="listbox"] li, 
    ul[role="listbox"] div,
    div[data-baseweb="popover"] span {
        color: #000000 !important;
        background-color: #ffffff !important;
    }

    div[role="option"]:hover,
    div[role="option"][aria-selected="true"],
    ul[role="listbox"] li:hover,
    ul[role="listbox"] li[aria-selected="true"] {
        background-color: #26a0da !important;
        color: #ffffff !important;
    }

    span[data-baseweb="tag"] {
        background-color: #26a0da !important;
        color: #ffffff !important;
    }
    span[data-baseweb="tag"] span {
        color: #ffffff !important;
    }
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
    div[data-testid="stBlock"] {
        background: rgba(255, 255, 255, 0.08) !important;
        padding: 20px !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    button[data-baseweb="tab"] {
        color: #ffffff !important;
        font-weight: bold !important;
        font-size: 16px !important;
    }
    button[aria-selected="true"] {
        color: #FFD700 !important;
        border-bottom-color: #FFD700 !important;
    }
    div[data-testid="stMetricValue"] {
        color: #FFD700 !important;
        font-size: 42px !important;
        font-weight: 800 !important;
    }

    /* --- ISOLATED INDEPENDENT 5 WHITE RESPONSE BOXES --- */
    /* Target and turn the 5 notification elements pure white so ticks and crosses display perfectly */
    div[data-testid="stNotificationV2"], 
    div[data-testid="stBaseAlert-success"],
    div[data-testid="stBaseAlert-danger"] {
        background-color: #1a2530 !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15) !important;
    }

    /* Set inner content texts to dark gray for high readability inside the white boxes */
    div[data-testid="stBaseAlert-success"] p,
    div[data-testid="stBaseAlert-success"] div,
    div[data-testid="stBaseAlert-danger"] p,
    div[data-testid="stBaseAlert-danger"] div {
        color: #ffffff !important;
        font-weight: 600 !important;
    }

    /* Give correct ticks and wrong cross marks distinct custom highlight borders */
    div[data-testid="stBaseAlert-success"] {
        border-left: 6px solid #2e7d32 !important;
    }
    div[data-testid="stBaseAlert-danger"] {
        border-left: 6px solid #c62828 !important;
    }
</style>
""", unsafe_allow_html=True)

LOGO_URL = "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiQ6lxEfFnImeGWEf7I7Fg9z-uCCkAdKWwxtHLn4zzcyCElV3DupEdwzEKpBin5ucTMpCLDbgwqN_cUkj7qhXDdgAIAvIFLdSJfl2byeN8e4_4oaVImEQQB9lYD-5qrC0mDqWWdXEFuhXy6jViTvcc-6LB6sJa3a2okWqasLjDKMoOxcbvtlUwCLxP5JEl6/s320/Gemini_Generated_Image_ce701rce701rce70-removebg-preview.png"

st.markdown(f"""
    <div class="branding-container">
        <img class="brand-logo" src="{LOGO_URL}" alt="MY SST ACADEMY LOGO">
        <div class="brand-text-block">
            <h1 class="main-academy-title">MY SST ACADEMY</h1>
            <p>Excellence in Social Science</p>
            <h2 class="sub-academy-title">CBSE Class X Map Works as per Academic Session: 2026-27</h2>
        </div>
    </div>
""", unsafe_allow_html=True)

st.write("Master your full 5 Marks syllabus items dynamically via outline map visualization or endless evaluation testing cycles.")

tabs = st.tabs(["👁️ Interactive Map Viewer", "📝 Infinite Practice Sets"])

# --- TAB 1: SYLLABUS LAYOUT VIEWER ---
with tabs[0]:
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("Syllabus Layout")
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
            folium.CircleMarker(
                location=coords,
                radius=8,
                popup=folium.Popup(f"<b>{item['name']}</b><br>State: {item['state']}", max_width=250),
                tooltip=item["name"],
                color="red" if "History" in category else "blue",
                fill=True,
                fill_opacity=0.7
            ).add_to(m)
        
        st_folium(m, width="100%", height=950)

# --- TAB 2: INFINITE PRACTICE ROOM ---
with tabs[1]:
    st.subheader("🧠 Unlimited Self-Assessment Test")
    st.write("Practise an infinite variety of combinations. Questions mirror identification styles seen in the board exam.")
    
    if "quiz_data" not in st.session_state:
        all_items = [(cat, item) for cat, items in MAP_DATA.items() for item in items]
        st.session_state.quiz_data = random.sample(all_items, min(5, len(all_items)))
        st.session_state.answers = {}
        st.session_state.submitted = False
        
        quiz_options = {}
        for idx, (cat, item) in enumerate(st.session_state.quiz_data):
            wrong_states = list(set([i["state"] for c, items in MAP_DATA.items() for i in items if i["state"] != item["state"]]))
            options = list(set([item["state"]] + random.sample(wrong_states, min(3, len(wrong_states)))))
            random.shuffle(options)
            quiz_options[idx] = options
        st.session_state.quiz_options = quiz_options

    if st.button("🔄 New Mock Test Set"):
        all_items = [(cat, item) for cat, items in MAP_DATA.items() for item in items]
        st.session_state.quiz_data = random.sample(all_items, 5)
        st.session_state.answers = {}
        st.session_state.submitted = False
        
        quiz_options = {}
        for idx, (cat, item) in enumerate(st.session_state.quiz_data):
            wrong_states = list(set([i["state"] for c, items in MAP_DATA.items() for i in items if i["state"] != item["state"]]))
            options = list(set([item["state"]] + random.sample(wrong_states, min(3, len(wrong_states)))))
            random.shuffle(options)
            quiz_options[idx] = options
        st.session_state.quiz_options = quiz_options
        st.rerun()

    for idx, (cat, item) in enumerate(st.session_state.quiz_data):
        st.markdown(f"**Question {idx+1}:** Identify the correct State/Territory where the listed feature **'{item['name']}'** (From *{cat}*) is located:")
        
        options = st.session_state.quiz_options[idx]
        user_choice = st.session_state.answers.get(idx)
        radio_index = options.index(user_choice) if user_choice in options else None
        
        st.session_state.answers[idx] = st.radio(
            f"Select positioning boundary for {item['name']}:", 
            options, 
            key=f"q_{idx}",
            index=radio_index
        )
        st.divider()

    st.markdown('<div id="evaluation-score-anchor"></div>', unsafe_allow_html=True)

    if st.button("📤 Submit Final Answer Sheet"):
        st.session_state.submitted = True

    if st.session_state.submitted:
        st.subheader("📊 Performance Summary & Analysis")
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

        js_scroll = """
        <script>
            var el = window.parent.document.getElementById("evaluation-score-anchor");
            if(el) {
                el.scrollIntoView({behavior: "smooth", block: "center"});
            }
        </script>
        """
        components.html(js_scroll, height=0, width=0)
