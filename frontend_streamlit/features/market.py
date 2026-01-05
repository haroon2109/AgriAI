import streamlit as st
import pandas as pd

@st.cache_data
def get_market_data():
    # Simulated Live Data from Agmarknet
    data = {
        "Commodity (பயிர்)": ["Paddy (நெல்)", "Tomato (தக்காளி)", "Cotton (பருத்தி)", "Turmeric (மஞ்சள்)", "Coconut (தேங்காய்)", "Banana (வாழை)"],
        "Market (சந்தை)": ["Madurai", "Dindigul", "Theni", "Erode", "Pollachi", "Trichy"],
        "Min Price (₹)": [1200, 1500, 4500, 6000, 25, 300],
        "Max Price (₹)": [1800, 2200, 5200, 7500, 35, 500],
        "Trend (போக்கு)": ["⬆️ High", "⬇️ Low", "➖ Stable", "⬆️ High", "➖ Stable", "⬆️ High"]
    }
    return pd.DataFrame(data)

def show_market():
    st.image("market_scene.png", use_container_width=True)
    st.title("🚜 Pasumai Sandhai (Green Marketplace)")
    
    # Tabs for Market Features
    tab1, tab2 = st.tabs(["📉 Market Prices", "📢 Report Price (விலை அறிக்கை)"])
    
    with tab2:
        st.info("💡 Help your village! Tell us the REAL price you sold at.")
        with st.form("price_report"):
            c1, c2 = st.columns(2)
            crop = c1.selectbox("Crop", ["Tomato", "Paddy", "Cotton"])
            price = c2.number_input("Sold Price (₹)", step=10)
            mandi = st.text_input("Mandi Name", "Local Sanda")
            
            if st.form_submit_button("Submit Report"):
                st.success(f"✅ Thank you! reported ₹{price} for {crop} at {mandi}")
                
        st.subheader("📢 Recent Farmer Reports")
        st.markdown("🔹 **Ramasamy** sold **Tomato** for **₹42/kg** at **Ottanchathiram** (10m ago)")
        st.markdown("🔹 **Kandasamy** sold **Paddy** for **₹1450/q** at **Thanjavur** (1h ago)")

    with tab1:
        st.subheader("Rentals & Services (வாடகை சேவை)")
    
    tab1, tab2 = st.tabs(["🚜 Machinery Rental ( இயந்திரம்)", "🌾 Sell Produce (விற்பனை)"])
    
    with tab1:
        st.caption("Quickly find tractors and drones nearby.")
        
        # Mock Tinder-style Card
        st.markdown("""
        <div style="
            max-width: 400px; margin: 0 auto; 
            border: 2px solid #ddd; border-radius: 20px; 
            overflow: hidden; box-shadow: 0 10px 20px rgba(0,0,0,0.2);
            background: white;
            text-align: center;">
            <img src="https://via.placeholder.com/400x250?text=Tractor+Mahindra+575" style="width:100%;">
            <div style="padding: 20px;">
                <h2 style="margin:0; color:#2E7D32;">Mahindra 575 DI</h2>
                <p style="color:gray;">Owned by: Murugan (2km away)</p>
                <div style="display:flex; justify-content:center; gap:10px; margin:10px 0;">
                    <span style="background:#E8F5E9; padding:5px 10px; border-radius:15px; font-size:12px;">Verified Owner ✅</span>
                    <span style="background:#FFF3E0; padding:5px 10px; border-radius:15px; font-size:12px;">Used by 15 Farmers 👥</span>
                </div>
                <h3 style="color:#BF360C;">₹800 / Hour</h3>
            </div>
            <div style="display:flex; border-top:1px solid #eee;">
                <button style="flex:1; padding:15px; border:none; background:white; color:red; font-size:20px; cursor:pointer;">✖️ Pass</button>
                <div style="width:1px; background:#eee;"></div>
                <button style="flex:1; padding:15px; border:none; background:white; color:green; font-size:20px; cursor:pointer;">📞 Booking</button>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        c_pass, c_book = st.columns(2)
        with c_pass:
            if st.button("✖️ Pass (வேண்டாம்)", use_container_width=True):
                st.toast("Skipped. Searching for next tractor...")
        with c_book:
            if st.button("📞 Book Now (அழைக்கவும்)", type="primary", use_container_width=True):
                st.balloons()
                st.success("Booking Request Sent to Owner Murugan! He will call you shortly.")
        
        st.info("Swipe functionality coming soon. Currently showing top tractor.")
        
    with tab2:
        st.subheader("📊 Live Mandi Prices (சந்தை நிலவரம்)")
        
        # --- HIGH IMPACT DASH-CARDS ---
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(label="தக்காளி (Tomato)", value="₹45", delta="2.50 ↑", delta_color="normal")
        with col2:
            st.metric(label="நெல் (Paddy)", value="₹2100", delta="-10.00 ↓", delta_color="inverse")
        with col3:
            st.metric(label="மஞ்சள் (Turmeric)", value="₹8500", delta="0.00", delta_color="off")

        st.markdown("---")
        st.caption("Source: Agmarknet (Simulated Data for Tamil Nadu)")
        
        # Mock Agmarknet Data integration
        mandi_data = [
            {"Commodity": "Tomato (தக்காளி)", "Market": "Oddanchatram", "Min": 4000, "Max": 4500, "Modal": 4200, "Unit": "Rs/Quintal"},
            {"Commodity": "Paddy (Common)", "Market": "Thanjavur", "Min": 2100, "Max": 2300, "Modal": 2250, "Unit": "Rs/Quintal"},
            {"Commodity": "Coconut", "Market": "Pollachi", "Min": 1200, "Max": 1500, "Modal": 1350, "Unit": "Rs/1000 Nuts"},
            {"Commodity": "Banana (Poovan)", "Market": "Trichy", "Min": 1500, "Max": 1800, "Modal": 1650, "Unit": "Rs/Quintal"},
            {"Commodity": "Onion (Small)", "Market": "Dindigul", "Min": 5000, "Max": 6000, "Modal": 5500, "Unit": "Rs/Quintal"},
        ]
        
        # Display as a clean table (Dataframe)
        import pandas as pd
        df = pd.DataFrame(mandi_data)
        st.dataframe(df, use_container_width=True)
        
        st.info("💡 **Trend:** Tomato prices are **Rising** (+5%) compared to yesterday due to rain in Andhra.")
        st.button("List my Harvest for Sale (விற்பனைக்கு இடு)")
