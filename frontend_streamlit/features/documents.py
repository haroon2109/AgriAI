import streamlit as st

def show_documents():
    st.title("🗂️ Digital Pattayam (Document Vault)")
    st.caption("Your Alamaari for Land Records (பாதுகாப்பான பெட்டகம்)")

    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.markdown("### 📄 My Documents (எனது ஆவணங்கள்)")
        
        docs = [
            {"name": "Patta Chitta (பட்டா சிட்டா)", "date": "Issued: Jan 2024", "status": "Active ✅"},
            {"name": "Crop Insurance (பயிர் காப்பீடு)", "date": "Expires: In 10 Days", "status": "Expiring ⚠️"},
            {"name": "Aadhaar Card", "date": "Verified", "status": "Active ✅"}
        ]
        
        for d in docs:
            bg = "#FFF3E0" if "Expiring" in d['status'] else "#F1F8E9"
            st.markdown(f"""
            <div style="background:{bg}; padding:15px; border-radius:10px; margin-bottom:10px; border:1px solid #ccc;">
                <div style="display:flex; justify-content:space-between;">
                    <h4 style="margin:0;">{d['name']}</h4>
                    <span>{d['status']}</span>
                </div>
                <p style="margin:5px 0; font-size:14px;">{d['date']}</p>
                <button>👁️ View</button> <button>🔗 Share</button>
            </div>
            """, unsafe_allow_html=True)
            
        st.divider()
        st.file_uploader("Upload New Document (புதிய ஆவணம்)", type=['pdf', 'jpg'])
        
    with c2:
        st.markdown("### 🔒 Security Status")
        st.success("All your documents are encrypted and safe.")
        st.markdown("---")
        st.markdown("### 🏦 Legacy Share")
        st.caption("Share verified details with Bank for Loan")
        if st.button("Generaly Bank Token"):
            st.info("Token Generated: AGRI-BANK-8821. Valid for 24 hours.")
        
    # Expiration Alert Logic (Mock)
    st.toast("⚠️ Reminder: Crop Insurance expires in 10 days!")
