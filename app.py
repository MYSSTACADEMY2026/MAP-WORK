# --- TAB 2: INFINITE PRACTICE ROOM ---
with tabs[1]:
    st.subheader("🧠 Unlimited Self-Assessment Test")
    st.write("Practise an infinite variety of combinations. Questions mirror identification styles seen in the board exam.")
    
    # 1. Initialize complete quiz state structural parameters securely
    if "quiz_data" not in st.session_state:
        all_items = [(cat, item) for cat, items in MAP_DATA.items() for item in items]
        st.session_state.quiz_data = random.sample(all_items, min(5, len(all_items)))
        st.session_state.answers = {}
        st.session_state.submitted = False
        
        # Lock options so they don't shift when a user clicks a radio button
        quiz_options = {}
        for idx, (cat, item) in enumerate(st.session_state.quiz_data):
            wrong_states = list(set([i["state"] for c, items in MAP_DATA.items() for i in items if i["state"] != item["state"]]))
            options = list(set([item["state"]] + random.sample(wrong_states, min(3, len(wrong_states)))))
            random.shuffle(options)
            quiz_options[idx] = options
        st.session_state.quiz_options = quiz_options

    # 2. Reset mechanism securely clears and regenerates quiz properties
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

    # 3. Render persistent elements from state
    for idx, (cat, item) in enumerate(st.session_state.quiz_data):
        st.markdown(f"**Question {idx+1}:** Identify the correct State/Territory where the listed feature **'{item['name']}'** (From *{cat}*) is located:")
        
        # Read protected choices directly from session state memory cache
        options = st.session_state.quiz_options[idx]
        
        # Capture option selection reliably
        st.session_state.answers[idx] = st.radio(
            f"Select positioning boundary for {item['name']}:", 
            options, 
            key=f"q_{idx}",
            index=None if idx not in st.session_state.answers else options.index(st.session_state.answers[idx])
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
