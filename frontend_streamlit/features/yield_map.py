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

    # 3. Render Map
    st_folium(m, width=800, height=500)
    
    # 4. Filter Controls
    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        st.selectbox("Select Crop Layer", ["Paddy", "Maize", "Cotton"])
    with c2:
    with c2:
        if st.button("🔄 Refresh Satellite Data (Live AI)"):
            backend_url = os.getenv("BACKEND_URL")
            if backend_url:
                try:
                    # Example API Call
                    payload = {"district_name": "Thanjavur", "crop": "Paddy"}
                    res = requests.post(f"{backend_url}/predict_yield", json=payload)
                    if res.status_code == 200:
                        data = res.json()
                        st.success(f"AI Prediction: {data['predicted_yield_kg_per_acre']} kg/acre")
                        st.json(data)
                    else:
                        st.error(f"API Error: {res.status_code}")
                except Exception as e:
                    st.error(f"Connection Failed: {e}")
            else:
                st.warning("Backend not connected (Running in Offline Mode)")
