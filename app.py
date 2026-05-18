import streamlit as st
import folium
from streamlit_folium import st_folium
import random
import streamlit.components.v1 as components

# --- COMPLETE CBSE MAP COORDINATES DATASET ---
COORDINATE_LOOKUP = {
    "Calcutta (Sept. 1920)": [22.5726, 88.3639],
    "Nagpur (Dec. 1920)": [21.1458, 79.0882],
    "Madras (1927)": [13.0827, 80.2707],
    "Champaran (Indigo Planters)": [26.8459, 84.5161],
    "Kheda (Peasant Satyagraha)": [22.7533, 72.6819],
    "Ahmedabad (Cotton Mill Workers)": [23.0225, 72.5714],
    "Jallianwala Bagh (Amritsar)": [31.6366, 74.8762],
    "Dandi (Civil Disobedience)": [20.8916, 72.7932],
    "Salal": [33.1534, 74.8148],
    "Bhakra Nangal": [31.4081, 76.4347],
    "Tehri": [30.3845, 78.4717],
    "Rana Pratap Sagar": [24.9228, 75.5804],
    "Sardar Sarovar": [21.8310, 73.7484],
    "Hirakud": [21.5362, 83.8697],
    "Nagarjuna Sagar": [16.5293, 79.3117],
    "Tungbhadra": [15.2530, 76.3409],
    "Mayurbhanj": [22.2400, 86.4300],
    "Durg": [21.1900, 81.2800],
    "Bailadila": [18.6214, 81.2494],
    "Bellary": [15.1394, 76.9214],
    "Kudremukh": [13.2181, 75.2479],
    "Raniganj": [23.6120, 87.1230],
    "Bokaro (Coal Mine)": [23.7957, 85.8290],
    "Talcher": [20.9520, 85.2282],
    "Neyveli": [11.5367, 79.4820],
    "Digboi": [27.3800, 95.6300],
    "Naharkatia": [27.2800, 95.3500],
    "Mumbai High": [19.4192, 71.3831],
    "Bassein": [19.3304, 72.8101],
    "Kalol": [23.2300, 72.4900],
    "Ankleshwar": [21.6200, 73.0200],
    "Namrup": [27.1800, 95.3900],
    "Singrauli": [24.1992, 82.6645],
    "Ramagundam": [18.8029, 79.4452],
    "Narora": [28.1929, 78.3886],
    "Kakrapar": [21.2655, 73.3512],
    "Tarapur": [19.8392, 72.7464],
    "Kalpakkam": [12.5574, 80.1581],
    "Mumbai (Cotton Textile)": [18.9220, 72.8346],
    "Indore": [22.7196, 75.8577],
    "Surat": [21.1702, 72.8311],
    "Kanpur": [26.4499, 80.3319],
    "Coimbatore": [11.0168, 76.9558],
    "Durgapur": [23.5204, 87.3119],
    "Bokaro (Iron & Steel)": [23.7957, 85.8290],
    "Jamshedpur": [22.8046, 86.2029],
    "Bhilai": [21.1938, 81.3509],
    "Vijayanagar": [15.1932, 76.6273],
    "Salem": [11.6643, 78.1460],
    "Noida": [28.5355, 77.3910],
    "Gandhinagar": [23.2156, 72.6369],
    "Mumbai (STP)": [19.0760, 72.8777],
    "Pune": [18.5204, 73.8567],
    "Hyderabad": [17.3850, 78.4867],
    "Bengaluru": [12.9716, 77.5946],
    "Chennai (STP)": [13.0827, 80.2707],
    "Thiruvananthapuram": [8.5241, 76.9366],
    "Kandla": [23.0300, 70.2200],
    "Mumbai (Port)": [18.9436, 72.8436],
    "Marmagao": [15.4078, 73.8014],
    "New Mangalore": [12.9347, 74.8194],
    "Kochi": [9.9312, 76.2673],
    "Tuticorin": [8.7642, 78.1348],
    "Chennai (Port)": [13.0924, 80.2974],
    "Vishakhapatnam": [17.6868, 83.2185],
    "Paradip": [20.2644, 86.6669],
    "Haldia": [22.0257, 88.0583],
    "Amritsar (Raja Sansi - Sri Guru Ram Das ji)": [31.7096, 74.8002],
    "Delhi (Indira Gandhi)": [28.5562, 77.1000],
    "Mumbai (Chhatrapati Shivaji)": [19.0896, 72.8656],
    "Chennai (Meenambakkam)": [12.9941, 80.1709],
    "Kolkata (Netaji Subhash Chandra Bose)": [22.6547, 88.4467],
    "Hyderabad (Rajiv Gandhi)": [17.2403, 78.4294]
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
       background: linear-gradient(180deg, #141419 0%, #24252a 55%, #3a3b45 100%) !important;
        color: #ffffff !important;
    }
    .branding-container {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 7px;
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
