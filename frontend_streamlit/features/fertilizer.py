import streamlit as st

def show_fertilizer():
    st.title("🧪 Ura-Kanakku (Smart Fertilizer)")
    st.caption("Avoid Over-Fertilization & Save Soil")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🌱 Crop Details")
        crop = st.selectbox("Select Crop", ["Paddy (Rice)", "Maize", "Cotton", "Sugarcane"])
        area = st.number_input("Field Area (Acres)", min_value=0.5, value=1.0)
        stage = st.selectbox("Growth Stage", ["Basal (Planting)", "Vegetative", "Flowering"])
        
        calc_btn = st.button("Calculate (கணக்கிடு)")
        
    with col2:
        if calc_btn:
             st.markdown("### ⚖️ Required Dosage")
             
             # Mock Calculation Logic
             urea_kg = area * 35 
             dap_kg = area * 15
             potash_kg = area * 10
             
             # Helper for Unit Conversion
             def to_bags(kg):
                 return round(kg / 50, 1) # Assuming 50kg bags
             
             st.info(f"Recommended for **{area} Acres** of **{crop}**:")
             
             st.markdown(f"""
             <div style="background:#E3F2FD; padding:15px; border-radius:10px; border-left:5px solid #1E88E5;">
                <h4>🧬 Urea</h4>
                <h2>{urea_kg} kg <span style="font-size:16px; color:#555;">(approx {to_bags(urea_kg)} Bags / Moodai)</span></h2>
             </div>
             <br>
             <div style="background:#E8F5E9; padding:15px; border-radius:10px; border-left:5px solid #43A047;">
                <h4>💪 DAP</h4>
                <h2>{dap_kg} kg <span style="font-size:16px; color:#555;">(approx {to_bags(dap_kg)} Bags / Moodai)</span></h2>
             </div>
             <br>
             <div style="background:#FFF3E0; padding:15px; border-radius:10px; border-left:5px solid #FB8C00;">
                <h4>🌺 Potash (MOP)</h4>
                <h2>{potash_kg} kg <span style="font-size:16px; color:#555;">(approx {to_bags(potash_kg)} Bags / Moodai)</span></h2>
             </div>
             """, unsafe_allow_html=True)
             
             st.warning("⚠️ **Farmer Tip:** Apply fertilizers 2 inches away from the root zone.")
        else:
            st.info("Enter details to see 'Mootai' (Bag) calculation.")
            # Animation Placeholder
            st.markdown("""
            <div style="text-align:center; opacity:0.5;">
                <h1 style="font-size:80px;">⚖️</h1>
                <p>Digital Weighing Scale Ready...</p>
            </div>
            """, unsafe_allow_html=True)
