import streamlit as st

def show_schemes():
    st.title("🏛️ Arasu Thittam (Govt. Schemes)")
    st.caption("AI Matchmaker for Government Subsidies")

    # Mock Database of Schemes
    schemes = [
        {
            "name": "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
            "desc": "Income support of ₹6,000/- per year in three equal installments.",
            "eligibility": "Small/Marginal Farmers (< 2 Hectares)",
            "benefit": "₹6,000 / Year",
            "link": "https://pmkisan.gov.in/"
        },
        {
            "name": "Kalaignarin All Village Integrated Agriculture Development Programme",
            "desc": "Distribution of coconut saplings, sprays, and vegetable seed kits.",
            "eligibility": "All Farmers in Selected Panchayats",
            "benefit": "Free Saplings & Kits",
            "link": "https://tn.gov.in"
        },
        {
            "name": "TNAU Drip Irrigation Subsidy",
            "desc": "Subsidy for installing drip/sprinkler irrigation systems.",
            "eligibility": "Small Farmers (100% Subsidy), Others (75%)",
            "benefit": "Up to 100% Subsidy",
            "link": "https://tnhorticulture.tn.gov.in/"
        }
    ]

    # --- Matchmaker Input Form ---
    with st.expander("🔍 Filter Criteria (தகுதி சோதிப்பு)", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            land_size = st.number_input("Land Size (Acres)", min_value=0.1, value=2.5)
        with c2:
            comm = st.selectbox("Category", ["Small/Marginal", "SC/ST", "Woman Farmer", "Others"])
    
    st.divider()

    # --- Results Display ---
    st.subheader("✅ Eligible Schemes (உங்களுக்கான திட்டங்கள்)")
    
    for s in schemes:
        # Simple Mock Logic for Demo
        is_eligible = True
        if "Small" in s['eligibility'] and land_size > 5:
            is_eligible = False
            
        if is_eligible:
            with st.container():
                st.markdown(f"""
                <div style="border: 1px solid #2E7D32; border-radius: 10px; padding: 15px; margin-bottom: 10px; background-color: #F1F8E9;">
                    <h3 style="color:#2E7D32; margin:0;">{s['name']}</h3>
                    <p><b>Benefit:</b> <span style="color:#BF360C; font-weight:bold;">{s['benefit']}</span></p>
                    <p style="font-size:14px;">{s['desc']}</p>
                    <a href="{s['link']}" target="_blank" style="text-decoration:none;">
                        <button style="background-color:#FFC107; border:none; padding:8px 15px; border-radius:5px; font-weight:bold; cursor:pointer;">
                             Apply Now (விண்ணப்பிக்க) 🏛️
                        </button>
                    </a>
                </div>
                """, unsafe_allow_html=True)
