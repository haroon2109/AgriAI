import streamlit as st
import pandas as pd
import time
import random

# Import local modules
import auth
import voice_engine

# --- Config & Setup ---
st.set_page_config(page_title="AgriAI", layout="wide", page_icon="🌾")

# Initialize DB
auth.init_db()

# --- TAMIL HERITAGE THEME (Mannum Marabum) ---
st.markdown("""
<style>
    /* Import Tamil Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Arima+Madurai:wght@700&family=Noto+Sans+Tamil:wght@400;700&display=swap');

    /* Global Background and Text */
    .stApp {
        background-color: #FAFAFA;
        font-family: 'Noto Sans Tamil', sans-serif;
    }

    /* Header Styling */
    h1, h2, h3 {
        font-family: 'Arima Madurai', cursive !important;
        color: #2E7D32 !important; /* Paddy Green */
    }

    /* Primary Buttons */
    .stButton>button {
        background-color: #BF360C !important; /* Terracotta Red */
        color: white !important;
        border-radius: 20px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
    }
    
    .stButton>button:hover {
        background-color: #FFC107 !important; /* Turmeric Gold */
        color: #2E7D32 !important;
    }

    /* Outline Button fix for Forms */
    .stFormSubmitButton>button {
        background-color: #BF360C !important;
        color: white !important;
        border: none !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #E8F5E9; /* Light Pacha Green */
    }
    
    /* Input Fields */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
        border: 2px solid #E0E0E0 !important;
        border-radius: 10px;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #FFFFFF;
        border-radius: 15px 15px 0 0;
        color: #2E7D32;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        background-color: #E8F5E9;
        border-bottom: 3px solid #BF360C;
    }

    /* Custom Card Style (Use with st.markdown) */
    .agri-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #FFC107;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    
    /* Loading Spinner Text */
    div[data-testid="stStatusWidget"] label {
        color: #BF360C !important;
        font-weight: bold;
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
            <h1 style="margin:0;">🌾 AgriAI</h1>
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
                        otp, err = auth.send_otp_email(email_input)
                        if otp:
                            st.session_state.otp_generated = otp
                            st.session_state.reset_phone = phone_assoc
                            st.session_state.forgot_step = 2
                            st.success(f"OTP sent to {email_input}")
                            st.rerun()
                        else:
                            st.error(f"Failed to send email: {err}")
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
        # --- HERO BANNER ---
        st.image("banner.png", use_container_width=True)
        
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
        st.subheader("📲 Quick Access (துரித சேவை)")
        
        # Grid Layout (2x2 for Big Buttons)
        r1_c1, r1_c2 = st.columns(2)
        r2_c1, r2_c2 = st.columns(2)
        
        # Tile 1: Scanner (Digital Maruthuvar)
        with r1_c1:
            st.image("scanner_tech.png", use_container_width=True)
            if st.button("📸 Digital Maruthuvar (Scanner)", use_container_width=True):
                st.session_state.page = "Digital Maruthuvar (Scanner)"
                st.rerun()

        # Tile 2: Market (Pasumai Sandhai)
        with r1_c2:
            st.image("market_scene.png", use_container_width=True)
            if st.button("💰 Pasumai Sandhai (Market)", use_container_width=True):
                st.session_state.page = "Pasumai Sandhai (Market)"
                st.rerun()
                
        # Tile 3: Advisor (Velaan-Thozhan)
        with r2_c1:
            st.image("advisor_mascot.png", use_container_width=True)
            if st.button("🤖 Velaan-Thozhan (Advisor)", use_container_width=True):
                st.session_state.page = "Velaan-Thozhan (Advisor)"
                st.rerun()
                
        # Tile 4: Weather/Crowdsourcing
        with r2_c2:
            st.image("https://images.unsplash.com/photo-1592210454359-9043f067919b", use_container_width=True) # Placeholder for Weather/General
            if st.button("🌧️ Weather & Schemes", use_container_width=True):
                 st.session_state.page = "Arasu Thittam (Schemes)"
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
