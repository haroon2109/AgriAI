import streamlit as st

def show_about():
    st.markdown("""
    <style>
        .quote-box {
            background-color: #E8F5E9;
            border-left: 5px solid #2E7D32;
            padding: 20px;
            font-style: italic;
            font-family: 'Times New Roman', serif;
            font-size: 18px;
        }
        .founder-note {
            font-family: 'Brush Script MT', cursive;
            font-size: 20px;
            color: #2D4628;
            margin-top: 10px;
        }
        .thinnai-card {
            background-color: #FFF3E0;
            padding: 20px;
            border-radius: 15px;
            border: 1px solid #FFC107;
            text-align: center;
        }
    </style>
    """, unsafe_allow_html=True)

    st.title("🌾 Mannum Manamum (Our Story)")
    st.subheader("மண்ணின் மரபும், அறிவியலின் ஆற்றலும்")
    
    # 1. ORIGN STORY (The Why)
    st.markdown("### வேர்கள் (Our Roots)")
    st.markdown("""
    <div class="quote-box">
    "உழுவார் உலகிற்கு அச்சாணி" (The farmer is the linchpin of the world)
    <br>- Thiruvalluvar
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    st.write("""
    **AgriAI** wasn't built in a lab; it was conceived in the fields. We believe that while farming is the oldest profession, 
    it deserves the world's newest technology. We are the bridge between the ancestral wisdom of the **Panchangam** and the precision of **Artificial Intelligence**.
    """)
    
    st.divider()
    
    # 2. TRADITION VS INNOVATION
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 🏛️ பாரம்பர்யம் (Tradition)")
        st.info("We honor the seasonal cycles of Aadi and Thai, respecting the natural instincts of the Tamil farmer.")
    with c2:
        st.markdown("### 🚀 புதுமை (Innovation)")
        st.success("We bring satellite data, disease detection, and real-time market insights to every farmer's pocket.")
        
    st.divider()
    
    # 3. MISSION (Digital Thinnai)
    st.markdown("### 🏘️ எங்கள் நோக்கம் (Our Mission)")
    st.markdown("""
    <div class="thinnai-card">
        <h3>The Digital Thinnai</h3>
        <p>To turn every smartphone into a village 'Thinnai' — a place for wisdom, support, and community.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # 4. FOUNDER'S NOTE
    st.markdown("### ✍️ Founder's Note")
    c_img, c_text = st.columns([1, 2])
    with c_img:
        st.markdown("👤") # Placeholder for sketch
    with c_text:
        st.write("\"We didn't build AgriAI to change how you farm; we built it to ensure that your children are proud to be farmers.\"")
        st.markdown('<p class="founder-note">- AgriAI Team (The Soil & Spirit)</p>', unsafe_allow_html=True)
