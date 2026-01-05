import streamlit as st

def show_videos():
    st.title("🎬 Velaan-Thirai (Agri-Cinemas)")
    st.caption("Short 60-second hacks for smart farming (Reels Style)")
    
    # Mock Video Data
    videos = [
        {"title": "Drip Filter Cleaning", "time": "45 sec", "img": "https://via.placeholder.com/150x250?text=Drip+Hack"},
        {"title": "Identify Armyworm", "time": "59 sec", "img": "https://via.placeholder.com/150x250?text=Pest+Check"},
        {"title": "Panchagavya Making", "time": "1 min", "img": "https://via.placeholder.com/150x250?text=Organic+Liquid"},
        {"title": "Solar Trap Setup", "time": "30 sec", "img": "https://via.placeholder.com/150x250?text=Light+Trap"}
    ]
    
    st.markdown("### 🔥 Trending Now (பிரபலமானவை)")
    
    cols = st.columns(4)
    
    for i, vid in enumerate(videos):
        with cols[i % 4]:
            st.markdown(f"""
            <div style="
                border-radius: 10px; overflow: hidden; 
                box-shadow: 0 4px 8px rgba(0,0,0,0.2); 
                background: white; position: relative; cursor: pointer;
                border: 1px solid #ddd;
                transition: transform 0.2s;">
                <img src="{vid['img']}" style="width:100%; opacity:1.0;">
                <div style="position:absolute; top:40%; left:40%; font-size:30px; background:rgba(255,255,255,0.7); border-radius:50%;">▶️</div>
                <div style="position:absolute; bottom:0; width:100%; background:rgba(255,255,255,0.9); color:black; padding:5px; font-size:12px; border-top:1px solid #ccc;">
                    <b>{vid['title']}</b><br>⏱️ {vid['time']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Watch {i+1}", key=f"vid_{i}"):
                st.video("https://www.youtube.com/watch?v=LXb3EKWsInQ") # Dummy link
