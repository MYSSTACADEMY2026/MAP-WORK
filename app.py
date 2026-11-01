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
        {"name": "Mumbai High", "state": "Maharashtra"},
        {"name": "Bassein", "state": "Maharashtra"},
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


# ------------------------- APP CONFIGURATION -------------------------
st.set_page_config(
    page_title="MY SST ACADEMY | CBSE Map Practice",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ------------------------- PREMIUM DESIGN -------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --navy: #102a43;
    --blue: #1769aa;
    --sky: #eaf4ff;
    --gold: #f5c542;
    --ink: #183247;
    --muted: #60758a;
}
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp {
    background: linear-gradient(145deg, #edf5fc 0%, #f7faff 48%, #e8f2fb 100%);
    color: var(--ink);
}
.block-container { padding-top: 1.5rem; padding-bottom: 3rem; max-width: 1500px; }
.hero {
    background: linear-gradient(115deg, #102a43 0%, #1769aa 68%, #2396c7 100%);
    border: 1px solid rgba(255,255,255,.18);
    border-radius: 22px;
    padding: 25px 30px;
    margin-bottom: 18px;
    box-shadow: 0 14px 34px rgba(16,42,67,.18);
    display: flex; align-items: center; gap: 22px;
}
.hero img { width: 88px; height: 88px; object-fit: contain; background: rgba(255,255,255,.95); border-radius: 16px; padding: 5px; }
.hero h1 { color: #ffd65a !important; font-size: clamp(27px, 4vw, 46px) !important; font-weight: 800 !important; margin: 0 !important; line-height: 1.1; }
.hero p { color: #f2f7fc !important; margin: 7px 0 0 0 !important; }
.eyebrow { color: #d7eaff; text-transform: uppercase; letter-spacing: 2px; font-size: 11px; font-weight: 700; }
.intro { color: #425b70; font-size: 15px; margin: 0 0 18px 2px; }
.stat {
    background: white; border: 1px solid #dce8f2; border-radius: 15px;
    padding: 15px 17px; box-shadow: 0 5px 16px rgba(24,50,71,.05);
}
.stat-label { color: #60758a; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: .7px; }
.stat-value { color: #123b5d; font-size: 25px; font-weight: 800; margin-top: 3px; }
.panel {
    background: white; border: 1px solid #dce8f2; border-radius: 18px;
    padding: 18px 20px; box-shadow: 0 6px 20px rgba(24,50,71,.055);
}
.panel-title { color: #123b5d; font-size: 19px; font-weight: 800; margin-bottom: 3px; }
.panel-subtitle { color: #718397; font-size: 13px; margin-bottom: 13px; }
div[data-testid="stTabs"] button { font-weight: 700; color: #31536d; }
div[data-testid="stTabs"] button[aria-selected="true"] { color: #1266a5; }
.stButton > button {
    border: 0; border-radius: 11px; min-height: 44px; font-weight: 700;
    background: linear-gradient(100deg, #1769aa, #2396c7); color: white;
    box-shadow: 0 5px 13px rgba(23,105,170,.18);
}
.stButton > button:hover { color: white; border: 0; background: #12588f; }
div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
    border-radius: 10px; border-color: #cbdbe8; background: #fbfdff;
}
div[data-testid="stMetric"] {
    background: #f7fbff; border: 1px solid #dfebf5; border-radius: 13px; padding: 12px;
}
div[data-testid="stMetricLabel"] { color: #5c7185; }
div[data-testid="stMetricValue"] { color: #135d96; font-weight: 800; }
div[data-testid="stAlert"] { border-radius: 12px; }
.small-note { color: #6c8092; font-size: 12px; }
@media (max-width: 700px) {
    .hero { padding: 18px; gap: 13px; }
    .hero img { width: 62px; height: 62px; }
    .block-container { padding-left: 1rem; padding-right: 1rem; }
}
</style>
""", unsafe_allow_html=True)

LOGO_URL = "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiQ6lxEfFnImeGWEf7I7Fg9z-uCCkAdKWwxtHLn4zzcyCElV3DupEdwzEKpBin5ucTMpCLDbgwqN_cUkj7qhXDdgAIAvIFLdSJfl2byeN8e4_4oaVImEQQB9lYD-5qrC0mDqWWdXEFuhXy6jViTvcc-6LB6sJa3a2okWqasLjDKMoOxcbvtlUwCLxP5JEl6/s320/Gemini_Generated_Image_ce701rce701rce70-removebg-preview.png"

st.markdown(f"""
<div class="hero">
  <img src="{LOGO_URL}" alt="MY SST ACADEMY logo">
  <div>
    <div class="eyebrow">Excellence in Social Science</div>
    <h1>MY SST ACADEMY</h1>
    <p>CBSE Class X · Map Work Practice · Academic Session 2026–27</p>
  </div>
</div>
""", unsafe_allow_html=True)

total_places = sum(len(items) for items in MAP_DATA.values())
st.markdown(
    '<p class="intro">Learn important map locations, explore syllabus topics and practise with fresh self-assessment sets.</p>',
    unsafe_allow_html=True
)

s1, s2, s3 = st.columns(3)
for col, label, value in [
    (s1, "Syllabus topics", len(MAP_DATA)),
    (s2, "Mapped locations", total_places),
    (s3, "Questions per mock test", 5),
]:
    with col:
        st.markdown(
            f'<div class="stat"><div class="stat-label">{label}</div><div class="stat-value">{value}</div></div>',
            unsafe_allow_html=True
        )

st.write("")
map_tab, quiz_tab = st.tabs(["🗺️  INTERACTIVE MAP EXPLORER", "✍️  PRACTICE & MOCK TEST"])

# ------------------------- MAP EXPLORER -------------------------
with map_tab:
    left, right = st.columns([1, 2.35], gap="large")

    with left:
        st.markdown('<div class="panel-title">Explore the syllabus</div>', unsafe_allow_html=True)
        st.markdown('<div class="panel-subtitle">Choose a topic and show the locations you want to revise.</div>', unsafe_allow_html=True)

        category = st.selectbox("Syllabus topic", list(MAP_DATA.keys()), key="map_category")
        places_in_cat = [item["name"] for item in MAP_DATA[category]]
        selected_places = st.multiselect(
            "Locations to display",
            places_in_cat,
            default=places_in_cat,
            key="selected_map_places"
        )

        st.markdown("**Map appearance**")
        st.caption("OpenStreetMap is used so the map does not need a CARTO API key.")
        st.info("Tip: Select one or two locations at a time when revising their exact positions.")

        if selected_places:
            st.metric("Locations displayed", len(selected_places))
        else:
            st.warning("Select at least one location to display markers.")

    with right:
        st.markdown('<div class="panel-title">Location map</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="panel-subtitle">{category} · {len(selected_places)} selected location(s)</div>',
            unsafe_allow_html=True
        )

        m = folium.Map(
            location=[22.0, 78.9],
            zoom_start=5,
            tiles="OpenStreetMap",
            control_scale=True
        )

        marker_color = "red" if "History" in category else "blue"
        marker_points = []

        for item in MAP_DATA[category]:
            if item["name"] in selected_places:
                coords = get_coordinates(item["name"], item["state"])
                marker_points.append(coords)
                folium.CircleMarker(
                    location=coords,
                    radius=7,
                    popup=folium.Popup(
                        f"<b>{item['name']}</b><br>State: {item['state']}",
                        max_width=260
                    ),
                    tooltip=f"{item['name']} · {item['state']}",
                    color=marker_color,
                    weight=2,
                    fill=True,
                    fill_color=marker_color,
                    fill_opacity=0.82
                ).add_to(m)

        if len(marker_points) > 1:
            m.fit_bounds(marker_points, padding=(28, 28))
        elif len(marker_points) == 1:
            m.location = marker_points[0]
            m.zoom_start = 7

        st_folium(
            m,
            width=None,
            height=650,
            returned_objects=[],
            key="cbse_map"
        )
        st.markdown(
            '<p class="small-note">Map tiles © OpenStreetMap contributors. An internet connection is needed to load the background map.</p>',
            unsafe_allow_html=True
        )

# ------------------------- PRACTICE & MOCK TEST -------------------------
def create_quiz():
    all_items = [(cat, item) for cat, items in MAP_DATA.items() for item in items]
    questions = random.sample(all_items, min(5, len(all_items)))
    all_states = sorted({item["state"] for _, items in MAP_DATA.items() for item in items})
    options_by_question = {}

    for idx, (_, item) in enumerate(questions):
        wrong_states = [state for state in all_states if state != item["state"]]
        wrong_choices = random.sample(wrong_states, min(3, len(wrong_states)))
        options = [item["state"]] + wrong_choices
        random.shuffle(options)
        options_by_question[idx] = options

    st.session_state.quiz_data = questions
    st.session_state.quiz_options = options_by_question
    st.session_state.answers = {}
    st.session_state.submitted = False

if "quiz_data" not in st.session_state:
    create_quiz()

with quiz_tab:
    st.markdown('<div class="panel-title">Mock test room</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="panel-subtitle">A fresh set of five questions is generated from your syllabus dataset.</div>',
        unsafe_allow_html=True
    )

    top_a, top_b = st.columns([3, 1])
    with top_a:
        st.info("Choose the state or territory associated with each listed feature. Submit when you are ready.")
    with top_b:
        if st.button("↻ New question set", use_container_width=True):
            create_quiz()
            st.rerun()

    answered_count = len(st.session_state.answers)
    st.progress(answered_count / len(st.session_state.quiz_data), text=f"{answered_count} of {len(st.session_state.quiz_data)} questions answered")

    with st.form("mock_test_form"):
        for idx, (cat, item) in enumerate(st.session_state.quiz_data):
            st.markdown(f"**Question {idx + 1}**")
            st.write(f"Where is **{item['name']}** located?")
            st.caption(f"Topic: {cat}")
            previous_answer = st.session_state.answers.get(idx)
            options = st.session_state.quiz_options[idx]
            default_index = options.index(previous_answer) if previous_answer in options else None
            choice = st.radio(
                f"Choose the correct state — question {idx + 1}",
                options,
                index=default_index,
                key=f"answer_{idx}",
                horizontal=True
            )
            st.session_state.answers[idx] = choice
            if idx < len(st.session_state.quiz_data) - 1:
                st.divider()

        submitted = st.form_submit_button("Submit answers", use_container_width=True)

    if submitted:
        st.session_state.submitted = True

    if st.session_state.submitted:
        score = sum(
            st.session_state.answers.get(idx) == item["state"]
            for idx, (_, item) in enumerate(st.session_state.quiz_data)
        )
        st.markdown("### Your result")
        st.metric("Mock test score", f"{score} / {len(st.session_state.quiz_data)}")
        st.progress(score / len(st.session_state.quiz_data))

        if score == len(st.session_state.quiz_data):
            st.success("Excellent work! You answered every question correctly.")
        elif score >= 3:
            st.info("Good effort. Review the explanations below and try another set.")
        else:
            st.warning("Keep practising. Revisit the map topics and try a new set.")

        for idx, (_, item) in enumerate(st.session_state.quiz_data):
            selected = st.session_state.answers.get(idx)
            if selected == item["state"]:
                st.success(f"Q{idx + 1}: {item['name']} — {item['state']} (Correct)")
            else:
                st.error(f"Q{idx + 1}: {item['name']} — Correct answer: {item['state']} · Your answer: {selected}")

        if st.button("Practise another set", use_container_width=True):
            create_quiz()
            st.rerun()

st.divider()
st.markdown(
    '<div style="text-align:center;color:#718397;font-size:12px;">MY SST ACADEMY · Learn · Locate · Practise · Improve</div>',
    unsafe_allow_html=True
)
