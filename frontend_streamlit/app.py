import streamlit as st
import pandas as pd
import time
import random

# Import local modules
import auth
import voice_engine

# --- Config & Setup ---
st.set_page_config(page_title="AgriAI Pro", layout="wide", page_icon="🌾")

# Initialize DB
auth.init_db()

# --- HIGH CONTRAST CSS (User Critical Request) ---
st.markdown("""
<style>
    /* Import Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Arima+Madurai:wght@300;400;700&family=Noto+Sans+Tamil:wght@300;400;700&display=swap');

    /* 1. Global Background */
    .stApp { 
        background-color: #F1F8E9; /* Light Pacha Green */
        font-family: 'Noto Sans Tamil', sans-serif;
    }
    
    /* Sidebar Background */
    section[data-testid="stSidebar"] {
        background-color: #DCEDC8; /* Slightly Darker Green */
    }

    /* 2. Typography - High Contrast */
    h1, h2, h3, h4, h5 { color: #2D4628 !important; font-family: 'Arima Madurai', cursive; }
    p, label, div, span { color: #1A1A1A !important; } /* Ebony Black for text */
    
    /* 3. Input Fields & Selectboxes - CRITICAL VISIBILITY FIX */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important; /* Pure White Bg */
        color: #1A1A1A !important;           /* Dark Ebony Text */
        caret-color: #BF360C !important;      /* Terracotta Cursor */
        border: 2px solid #D1D5DB !important; /* Light Grey Border */
        border-radius: 8px;
        font-weight: 500;
    }
    
    /* Force dropdown menu options to be visible */
    ul[data-testid="stSelectboxVirtualDropdown"] li {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
    }

    /* 4. Labels */
    .stTextInput label, .stSelectbox label {
        color: #2D4628 !important; /* Forest Green Labels */
        font-weight: 700 !important;
        font-size: 16px !important;
    }

    /* 5. Buttons (All Types) - White & Green */
    .stButton>button, .stFormSubmitButton>button {
        background-color: #FFFFFF !important;
        color: #2D4628 !important;
        border: 2px solid #2D4628 !important;
        border-radius: 8px;
        font-weight: bold;
    }
    .stButton>button:hover, .stFormSubmitButton>button:hover {
        background-color: #2D4628 !important;
        color: #FFFFFF !important;
        border-color: #2D4628 !important;
    }

    /* 6. Tabs styling */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px; white-space: pre-wrap;
        background-color: #FFFFFF; border-radius: 5px;
        color: #2D4628;
    }
    .stTabs [aria-selected="true"] {
        background-color: #E8F5E9; border-bottom: 2px solid #2D4628;
    }

    /* 7. Sidebar Toggle Button Fix */
    button[kind="header"], [data-testid="collapsedControl"] {
        background-color: #DCEDC8 !important; /* Light Green */
        color: #2D4628 !important; /* Dark Green Icon */
        border: 1px solid #2D4628 !important;
        border-radius: 8px;
    }
    
    /* 8. AGGRESSIVE LIGHT MODE FORCE */
    /* Ensure no dark backgrounds persist */
    .stApp, div[data-testid="stDecoration"], div[data-testid="stToolbar"], div[data-testid="stHeader"] {
        background-color: #F1F8E9 !important;
    }
    
    /* Force Text Color Black */
    body, p, div, span, h1, h2, h3, h4, h5, h6, label, li, a {
        color: #000000 !important;
    }
    
    /* Fix Input Fields appearing dark */
    input, textarea, select {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    
    /* Fix SVGs turning white in dark mode */
    svg {
        fill: #000000 !important;
        stroke: #000000 !important;
    }
    
    /* Specific overrides for Streamlit Containers */
    div[data-testid="stSidebar"] {
        background-color: #DCEDC8 !important;
    }
</style>
""", unsafe_allow_html=True)


# --- SESSION STATE ---
if "user" not in st.session_state: st.session_state.user = None
if "page" not in st.session_state: st.session_state.page = "Mugappu"

# --- AUTH CARD COMPONENT ---
def auth_card():
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.5, 1]) # Centered Layout
    
    with c2:
        st.markdown(f"""
        <div style="text-align:center; padding:20px; border:2px solid #2D4628; border-radius:15px; background:white; margin-bottom:20px;">
            <h1 style="margin:0;">🌾 AgriAI Pro</h1>
            <p>Mannum Marabum Edition</p>
        </div>
        """, unsafe_allow_html=True)
        
        tab_login, tab_reg, tab_forgot = st.tabs(["🔐 Login (புகு)", "📝 Register (பதிவு)", "❓ Forgot"])
        
        with tab_login:
            with st.form("login_form"):
                phone = st.text_input("Mobile Number (கைபேசி எண்)")
                password = st.text_input("Password (கடவுச்சொல்)", type="password")
                if st.form_submit_button("Login (உள்ளே செல்)"):
                    user = auth.login_user(phone, password)
                    if user:
                        st.session_state.user = user
                        st.success("Welcome back!")
                        time.sleep(0.5)
                        st.rerun()
                    else:
                        st.error("Invalid Credentials. Please try again.")

        with tab_reg:
            with st.form("reg_form"):
                name = st.text_input("Full Name (பெயர்)")
                phone_reg = st.text_input("Mobile (10 Digits)")
                email = st.text_input("Email (For Recovery)")
                city = st.text_input("Village / City (ஊர்)")
                dist = st.selectbox("District (மாவட்டம்) ▼", [
                    "Ariyalur", "Chengalpattu", "Chennai", "Coimbatore", "Cuddalore", "Dharmapuri", 
                    "Dindigul", "Erode", "Kallakurichi", "Kancheepuram", "Karur", "Krishnagiri", 
                    "Madurai", "Mayiladuthurai", "Nagapattinam", "Kanyakumari", "Namakkal", 
                    "Perambalur", "Pudukkottai", "Ramanathapuram", "Ranipet", "Salem", "Sivagangai", 
                    "Tenkasi", "Thanjavur", "Theni", "The Nilgiris", "Thiruvallur", "Thiruvarur", 
                    "Thoothukudi", "Tiruchirappalli", "Tirunelveli", "Tirupathur", "Tiruppur", 
                    "Tiruvannamalai", "Vellore", "Viluppuram", "Virudhunagar"
                ])
                pass_reg = st.text_input("Create Password", type="password")
                
                if st.form_submit_button("Create Account"):
                    ok, msg = auth.register_user(name, phone_reg, email, city, dist, pass_reg)
                    if ok:
                        st.success("Registration Successful! Please Login.")
                    else:
                        st.error(msg)
        
        with tab_forgot:
            st.write("🔄 **Reset Password (கடவுச்சொல் மீட்பு)**")
            
            if "forgot_step" not in st.session_state:
                st.session_state.forgot_step = 1
            
            # Step 1: Input Email
            if st.session_state.forgot_step == 1:
                email_input = st.text_input("Enter Registered Email")
                if st.button("Send OTP"):
                    phone_assoc = auth.check_email_exists(email_input)
                    if phone_assoc:
                        # Send Email
                        otp = auth.send_otp_email(email_input)
                        if otp:
                            st.session_state.otp_generated = otp
                            st.session_state.reset_phone = phone_assoc
                            st.session_state.forgot_step = 2
                            st.success(f"OTP sent to {email_input}")
                            st.rerun()
                        else:
                            st.error("Failed to send email. Check API Password.")
                    else:
                        st.error("Email not found!")
            
            # Step 2: Verify OTP
            elif st.session_state.forgot_step == 2:
                otp_input = st.text_input("Enter 4-Digit OTP")
                if st.button("Verify OTP"):
                    if otp_input == st.session_state.otp_generated:
                        st.success("Verified!")
                        st.session_state.forgot_step = 3
                        st.rerun()
                    else:
                        st.error("Invalid OTP")
            
            # Step 3: New Password
            elif st.session_state.forgot_step == 3:
                new_pass = st.text_input("New Password", type="password")
                confirm_pass = st.text_input("Confirm Password", type="password")
                
                if st.button("Change Password"):
                    if new_pass == confirm_pass and len(new_pass) > 3:
                        auth.update_password(st.session_state.reset_phone, new_pass)
                        st.success("Password Updated! Please Login.")
                        st.session_state.forgot_step = 1
                    else:
                        st.error("Passwords must match and be > 3 chars")

# Import local features
import features.scanner as scanner
import features.about as about
import features.community as community
import features.schemes as schemes
import features.fertilizer as fertilizer
import features.videos as videos
import features.pricing as pricing
import features.advisor as advisor
import features.documents as documents
import features.market as market
import features.yield_map as yield_map

# --- MAIN APP FLOW ---
if not st.session_state.user:
    auth_card()
else:
    # --- DASHBOARD (Only visible after login) ---
    
    # Sidebar
    with st.sidebar:
        st.title(f"👨🏾‍🌾 {st.session_state.user['name']}")
        st.caption(f"📍 {st.session_state.user['district']}")
        
        # Dialect Selection
        st.selectbox("🗣️ Voice Dialect", ["General Tamil", "Kongu Tamil", "Nellai Tamil", "Madurai Tamil"])
        
        # Sunlight Mode Toggle
        sunlight_mode = st.toggle("☀️ Sunlight Mode (வெயில் நேரம்)")
        if sunlight_mode:
            st.markdown("""
            <style>
                .stApp { background-color: #FFFFFF !important; }
                h1, h2, h3, h4, h5, p, div, span, label { color: #000000 !important; font-weight: 900 !important; }
                /* Updated: High Contrast White Mode */
                .stButton>button { background-color: #FFFFFF !important; color: #000000 !important; border: 2px solid #2D4628 !important; }
                .stTextInput>div>div>input { background-color: #FFFFFF !important; color: #000000 !important; border: 2px solid #2D4628 !important; }
                /* Ensure selectboxes are also white */
                .stSelectbox>div>div>div { background-color: #FFFFFF !important; color: #000000 !important; border: 2px solid #2D4628 !important; }
                /* Force SVG Arrow to be Dark Green */
                div[data-baseweb="select"] svg { fill: #2D4628 !important; }
            </style>
            """, unsafe_allow_html=True)
        
        # Navigation Menu
        nav = st.radio("Menu", [
            "Mugappu (Home)", 
            "Digital Maruthuvar (Scanner)", 
            "Velaan-Thozhan (Advisor)",
            "Uzhavar Sangamam (Community)",
            "Pasumai Sandhai (Market)", 
            "Arasu Thittam (Schemes)",
            "Digital Pattayam (Docs)",
            "Ura-Kanakku (Fertilizer)",
            "Velaan-Thirai (Videos)",
            "Sat-Map (Yield Forecast)",
            "Pattam Pricing (Plans)",
            "Mannum Manamum (About Us)"
        ])
        st.session_state.page = nav
        st.divider()
        if st.button("Logout"):
            st.session_state.user = None
            st.rerun()
    
    # Page Routing
    pg = st.session_state.page
    
    if "Mugappu" in pg:
        st.title("Mugappu (Home)")
        
        # Weather Widget with Crowdsourcing
        c1, c2 = st.columns([3, 1])
        with c1:
            st.info(f"🌤️ **Weather in {st.session_state.user['district']}:** 32°C, Partly Cloudy.")
        with c2:
            if st.button("🌧️ Report Rain"):
                st.toast("Thanks! Your report helps the village.")
                
        st.write("Current **Thai Pattam** Season is active. (Harvest Phase)")
        st.divider()
        
        # --- QUICK ACCESS LAUNCHPAD (துரித சேவை) ---
        st.subheader("Quick Access (துரித சேவை)")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("<div style='text-align:center; font-size:40px;'>🌿</div>", unsafe_allow_html=True)
            if st.button("Digital Maruthuvar", key="btn_scan"):
                st.session_state.page = "Digital Maruthuvar (Scanner)"
                st.rerun()

        with col2:
            st.markdown("<div style='text-align:center; font-size:40px;'>💰</div>", unsafe_allow_html=True)
            if st.button("Pasumai Sandhai", key="btn_market"):
                st.session_state.page = "Pasumai Sandhai (Market)"
                st.rerun()
                
        with col3:
            st.markdown("<div style='text-align:center; font-size:40px;'>🤖</div>", unsafe_allow_html=True)
            if st.button("Velaan-Thozhan", key="btn_advisor"):
                st.session_state.page = "Velaan-Thozhan (Advisor)"
                st.rerun()
                
        st.write("")
        col4, col5, col6 = st.columns(3)
        
        with col4:
            st.markdown("<div style='text-align:center; font-size:40px;'>🧪</div>", unsafe_allow_html=True)
            if st.button("Ura-Kanakku", key="btn_fert"):
                st.session_state.page = "Ura-Kanakku (Fertilizer)"
                st.rerun()
        
        with col5:
            st.markdown("<div style='text-align:center; font-size:40px;'>🏛️</div>", unsafe_allow_html=True)
            if st.button("Arasu Thittam", key="btn_scheme"):
                st.session_state.page = "Arasu Thittam (Schemes)"
                st.rerun()
                
        with col6:
            st.markdown("<div style='text-align:center; font-size:40px;'>🗂️</div>", unsafe_allow_html=True)
            if st.button("Digital Pattayam", key="btn_docs"):
                st.session_state.page = "Digital Pattayam (Docs)"
                st.rerun()
        
    elif "Digital Maruthuvar" in pg:
        scanner.show_scanner()

    elif "Schemes" in pg:
        schemes.show_schemes()
        
    elif "Fertilizer" in pg:
        fertilizer.show_fertilizer()

    elif "Videos" in pg:
        videos.show_videos()
        
    elif "Community" in pg:
        community.show_community()

    elif "Market" in pg:
        market.show_market()
        
    elif "Advisor" in pg:
        advisor.show_advisor()

    elif "Docs" in pg:
        documents.show_documents()

    elif "Yield Forecast" in pg:
        yield_map.show_yield_map()
        
    elif "Pricing" in pg:
        pricing.show_pricing()
        
    elif "About" in pg:
        about.show_about()
