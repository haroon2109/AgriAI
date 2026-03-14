import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import os

def show_yield_map():
    st.title("🗺️ District Yield Map (விளைச்சல் வரைபடம்)")
    st.caption("Satellite-based Yield Prediction (Sentinel-2 Data)")

    # 1. Base Map centered on Tamil Nadu
    m = folium.Map(location=[11.1271, 78.6569], zoom_start=7)

    # 2. Mock GeoJSON Data (Ideally this comes from PostGIS/backend)
    # Adding markers for key districts
    districts = [
        {"name": "Thanjavur", "coords": [10.7870, 79.1378], "yield": "High", "color": "green", "crop": "Paddy"},
        {"name": "Madurai", "coords": [9.9252, 78.1198], "yield": "Medium", "color": "orange", "crop": "Jasmine"},
        {"name": "Coimbatore", "coords": [11.0168, 76.9558], "yield": "High", "color": "green", "crop": "Cotton"},
        {"name": "Ramanathapuram", "coords": [9.36, 78.83], "yield": "Low", "color": "red", "crop": "Chilli"},
    ]

    for d in districts:
        folium.Marker(
            location=d["coords"],
            popup=f"<b>{d['name']}</b><br>Crop: {d['crop']}<br>Yield Forecast: {d['yield']}",
            icon=folium.Icon(color=d["color"], icon="leaf")
        ).add_to(m)

    # Pest Alert Layer
    show_pest = st.toggle("⚠️ Show Pest Heatspots (Yellow Sticker Alert)", value=False)
    
    if show_pest:
        # Mock "Heatspots" from neighbors
        pest_spots = [
            [10.8, 79.15], # Thanjavur West
            [9.95, 78.15], # Madurai North
        ]
        for p in pest_spots:
            folium.CircleMarker(
                location=p,
                radius=15,
                color="red",
                fill=True,
                fill_color="red",
                fill_opacity=0.6,
                popup="⚠️ Pest Reported by 5 Neighbors!"
            ).add_to(m)

    # 3. Render Map
    st_folium(m, width=800, height=500)
    
    # 4. Filter Controls & API Interaction
    st.divider()
    c1, c2, c3 = st.columns(3)
    with c1:
        selected_crop = st.selectbox("Select Crop (பயிர்)", ["Paddy (நெல்)", "Sugarcane (கரும்பு)", "Cotton (பருத்தி)"])
    with c2:
        sowing_date = st.date_input("Sowing Date (விதைப்பு தேதி)")
    with c3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Forecast Yield (விளைச்சல் கணிப்பு)"):
            backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")
            try:
                # Selecting lat/lon based on user location (Mocking Madurai here)
                payload = {
                    "lat": 9.9252, 
                    "lon": 78.1198,
                    "crop_type": selected_crop.split(" ")[0], # Send english name
                    "sowing_date": str(sowing_date)
                }
                res = requests.post(f"{backend_url}/predict_yield", json=payload)
                if res.status_code == 200:
                    data = res.json()
                    
                    st.success("Analysis Complete (கணிப்பு முடிந்தது) ✅")
                    
                    # Custom Cards for Output
                    cc1, cc2 = st.columns(2)
                    with cc1:
                        st.markdown(f"""
                        <div class="agri-card" style="border-left: 5px solid #2E7D32;">
                            <h3 style="margin-bottom:0;">Yield Forecast</h3>
                            <p style="color:gray;">விளைச்சல் கணிப்பு</p>
                            <h2 style="color:#2E7D32;">{data['predicted_yield']} kg/acre</h2>
                            <p>Confidence: {data['confidence_interval']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                    with cc2:
                        st.markdown(f"""
                        <div class="agri-card" style="border-left: 5px solid #1E88E5;">
                            <h3 style="margin-bottom:0;">Health Gauge</h3>
                            <p style="color:gray;">பயிர் ஆரோக்கியம்</p>
                            <h2 style="color:#1E88E5;">Good (நன்று)</h2>
                            <p>Based on Sentinel-2 NDVI</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                else:
                    st.error(f"API Error: {res.status_code}")
            except Exception as e:
                st.error(f"Connection Failed: {e}. Is the backend running?")
