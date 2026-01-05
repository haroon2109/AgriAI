import streamlit as st

def show_pricing():
    st.title("🎫 Pattam Pricing (பருவ இதழ் சந்தா)")
    st.caption("Pay once per harvest season. No hidden monthly fees.")
    
    # --- Comparison Table ---
    c1, c2, c3 = st.columns(3)
    
    # FREE PLAN
    with c1:
        st.markdown("""
        <div style="border:1px solid #ddd; padding:20px; border-radius:10px; text-align:center;">
            <h3>🆓 Aarambam</h3>
            <h1 style="color:#2E7D32;">₹0</h1>
            <p>Forever Free</p>
            <hr>
            <ul style="text-align:left;">
                <li>✅ 5 Disease Scans/Mo</li>
                <li>✅ Basic Weather</li>
                <li>✅ Mandi Prices</li>
            </ul>
            <button style="width:100%; padding:10px; background:#e0e0e0; border:none; border-radius:5px;">Current Plan</button>
        </div>
        """, unsafe_allow_html=True)
        
    # PRO PLAN
    with c2:
        st.markdown("""
        <div style="border:2px solid #FFC107; padding:20px; border-radius:10px; text-align:center; background:#FFFDE7; position:relative;">
            <div style="position:absolute; top:-10px; right:10px; background:#FFC107; padding:2px 10px; border-radius:10px; font-size:12px; font-weight:bold;">BEST VALUE</div>
            <h3>🌾 Vilaichal</h3>
            <h1 style="color:#BF360C;">₹299</h1>
            <p>Per Season (4 Months)</p>
            <hr>
            <ul style="text-align:left;">
                <li>✅ <b>Unlimited</b> Scans</li>
                <li>✅ <b>Expert</b> Consultation</li>
                <li>✅ <b>Govt Scheme</b> Autofill</li>
            </ul>
            <button style="width:100%; padding:10px; background:#2E7D32; color:white; border:none; border-radius:5px; font-weight:bold;">Select Plan</button>
        </div>
        """, unsafe_allow_html=True)
        
    # ENTERPRISE
    with c3:
        st.markdown("""
        <div style="border:1px solid #ddd; padding:20px; border-radius:10px; text-align:center;">
            <h3>🚜 Munodi</h3>
            <h1 style="color:#1A237E;">₹999</h1>
            <p>Per Year</p>
            <hr>
            <ul style="text-align:left;">
                <li>✅ Soil Testing Kit</li>
                <li>✅ IoT Sensor Support</li>
                <li>✅ Dedicated Manager</li>
            </ul>
            <button style="width:100%; padding:10px; background:#1A237E; color:white; border:none; border-radius:5px;">Contact Us</button>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    
    # --- Value Calculator ---
    st.subheader("💡 Why pay ₹299?")
    st.info("Let's calculate your savings for one season (ஒரு பட்டத்தின் சேமிப்பு).")
    
    col_calc, col_res = st.columns(2)
    with col_calc:
        pest_save = st.slider("Money wasted on wrong pesticides?", 500, 5000, 2000)
        fert_save = st.slider("Money wasted on extra fertilizer?", 500, 5000, 1500)
        
    with col_res:
        total_save = pest_save + fert_save
        roi = round((total_save - 299) / 299 * 100)
        st.metric("Total Potential Savings", f"₹ {total_save}", delta=f"{roi}% ROI")
        st.caption(f"You pay only ₹299 to save ₹{total_save}!")
        
    st.divider()
    
    # --- Payment Section ---
    st.subheader("💳 Easy Payment (கிராமத்து முறை)")
    cp1, cp2 = st.columns(2)
    with cp1:
        st.image("https://via.placeholder.com/150x150?text=QR+Code", caption="Scan with GPay/PhonePe")
    with cp2:
        st.checkbox("🌾 Pay After Harvest (Commitment Fee ₹50)")
        st.markdown("**Gift a Farmer:** Buy a subscription for your parents in the village.")
        st.button("🎁 Gift Now")
