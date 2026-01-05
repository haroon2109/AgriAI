import streamlit as st

def show_community():
    st.title("🌳 Uzhavar Sangamam (Community)")
    st.caption("A Digital Banyan Tree for Farmers (உழவர் சந்தை)")
    
    # --- Palamozhi Ticker ---
    st.info("📢 **Today's Proverb:** 'அகல உழுவதை விட ஆழ உழுவதே மேல்' (Deep ploughing is better than wide ploughing).")
    
    # --- District Hub Auto-Join ---
    user_dist = st.session_state.user['district'] if st.session_state.user else "Tamil Nadu"
    st.success(f"📍 You are viewing the **{user_dist} Farmers Group**")
    
    # --- Gamification Header ---
    points = 120 # Mock points
    st.markdown(f"🏆 **Your Harvest Points:** {points} (Level: முன்னோடி விவசாயி)")
    
    st.divider()
    
    # --- Top Discussions ---
    st.subheader("🔥 Trending Now (இப்போதைய விவாதம்)")
    
    with st.expander("🌡️ How to handle upcoming summer heat? (45 replies)", expanded=True):
        st.write("**Ramasamy (Pollachi):** I am using drip irrigation at night. Very effective.")
        st.write("**Kumar (Theni):** Mulching is saving my crops.")
        if st.button("👍 Vazhthukkal (Kudos)"):
            st.toast("You appreciated this post! (+5 Points)")
            
    with st.expander("🐛 Fall Armyworm spotted in Madurai East"):
        st.warning("⚠️ 3 farmers reported this in your area.")
        st.write("**Expert officer:** Please check your maize crops immediately.")
    
    st.divider()
    
    # --- Success Stories ---
    st.subheader("🎉 Success Stories (வெற்றி கதைகள்)")
    c1, c2 = st.columns(2)
    with c1:
        st.image("https://via.placeholder.com/300x200?text=Bumper+Harvest", caption="Velu's Bumper Tomato Harvest")
        if st.button("❤️ Vazhthukkal (Velu)"):
            st.balloons()
    with c2:
        st.write("Velu from Dindigul saved 20% on fertilizers using AgriAI's calculator!")
        
    st.divider()
    
    # --- Ask Community ---
    st.subheader("🗣️ Ask the Community (கேள்வி கேளுங்கள்)")
    st.text_input("Title", placeholder="Eg. My coconut trees are yellowing...")
    st.text_area("Details", placeholder="Describe the issue...")
    st.markdown("**🎙️ Or Record a Voice Note:**")
    st.button("🎤 Start Recording")
