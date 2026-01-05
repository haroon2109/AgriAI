import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import re
import sqlite3
import hashlib
import time
import random

# --- Config & Setup ---
st.set_page_config(page_title="AgriAI Pro", layout="wide", page_icon="🌾")

# --- PACHA-MANN PRO THEME (High Contrast) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Tamil:wght@300;400;700&family=Inter:wght@300;400;700&display=swap');

    /* 1. Main Background: Sand Cream */
    .stApp { background-color: #FDFBF7; font-family: 'Noto Sans Tamil', 'Inter', sans-serif; }
    
    /* 2. Text Colors (Strict High Contrast) */
    h1, h2, h3, h4, h5 { color: #4A3728 !important; font-weight: 700; }
    p, div, label, span, li { color: #2D4628 !important; }
    
    /* 3. Inputs: Pure White Background + Dark Text + Visible Caret */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: #FFFFFF !important;
        color: #4A3728 !important;
        caret-color: #4A3728 !important; /* The typing line (|) */
        border: 1px solid #D4AF37;
        border-radius: 10px;
    }
    
    /* Fix Password Eye Icon & other input icons */
    button[aria-label="Show password"] {
        color: #4A3728 !important;
    }
    div[data-baseweb="base-input"] svg {
        fill: #4A3728 !important;
    }
    
    /* 4. Cards: White Glassmorphism */
    div.stMetric, div.css-1r6slb0, div[data-testid="stExpander"], div.stForm {
        background: #FFFFFF;
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 5px 20px rgba(45, 70, 40, 0.08);
    }
    
    /* 5. Buttons: Universal White High Contrast */
    .stButton>button, .stDownloadButton>button, .stFormSubmitButton>button, button[kind="primary"], button[kind="secondary"] {
        background-color: #FFFFFF !important; 
        color: #2D4628 !important;
        border: 2px solid #2D4628 !important; 
        border-radius: 10px;
        font-weight: 700;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover, .stDownloadButton>button:hover, .stFormSubmitButton>button:hover, button[kind="primary"]:hover, button[kind="secondary"]:hover {
        background-color: #F0F5F0 !important; /* Very Light Green Hover */
        color: #2D4628 !important;
        border-color: #D4AF37 !important;
        transform: translateY(-2px);
    }

    /* 6. Icon Box */
    .icon-box {
        background: #FFFFFF;
        border-radius: 20px;
        padding: 10px;
        width: 80px; height: 80px;
        display: flex; align-items: center; justify-content: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        border: 2px solid #D4AF37;
    }
    
    /* 7. Pongal Animation */
    @keyframes float { 0% { transform: translateY(0px); } 50% { transform: translateY(-10px); } 100% { transform: translateY(0px); } }
    .pongal-anim { font-size: 40px; animation: float 3s ease-in-out infinite; }
    
    /* 8. Success/Error Message Text */
    .stAlert { font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- DATABASE (agri_pro.db) ---
DB_PATH = "agri_pro.db"
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, phone TEXT UNIQUE NOT NULL,
                    email TEXT, city TEXT NOT NULL, district TEXT NOT NULL, password_hash TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def hash_password(password): return hashlib.sha256(password.encode()).hexdigest()

def db_register(name, phone, email, city, district, password):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO users (name, phone, email, city, district, password_hash) VALUES (?, ?, ?, ?, ?, ?)",
                  (name, phone, email, city, district, hash_password(password)))
        conn.commit()
        conn.close()
        return True, "Success"
    except sqlite3.IntegrityError: return False, "Phone Number already registered."

def db_login(phone, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE phone = ? AND password_hash = ?", (phone, hash_password(password)))
    user = c.fetchone()
    conn.close()
    if user: return {"name": user[1], "phone": user[2], "email": user[3], "city": user[4], "district": user[5]}
    return None

def db_check_email(email):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT phone FROM users WHERE email = ?", (email,))
    user = c.fetchone()
    conn.close()
    return user[0] if user else None

def db_update_password(phone, new_password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET password_hash = ? WHERE phone = ?", (hash_password(new_password), phone))
    conn.commit()
    conn.close()

# --- INIT STATE ---
init_db()
if "user" not in st.session_state: st.session_state.user = None
if "auth_mode" not in st.session_state: st.session_state.auth_mode = "login" # login, register, forgot, reset
if "reset_email" not in st.session_state: st.session_state.reset_email = None
if "reset_code" not in st.session_state: st.session_state.reset_code = None
if "page" not in st.session_state: st.session_state.page = "Dashboard"
if "lang" not in st.session_state: st.session_state.lang = "English"

# --- AUTH FLOW ---
def auth_container():
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("<h1 style='text-align:center;'>🌾 AgriAI Pro</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;'>Professional Decision Support System</p>", unsafe_allow_html=True)
        
        mode = st.session_state.auth_mode
        
        # 1. LOGIN
        if mode == "login":
            with st.form("login_form"):
                st.subheader("Login to Dashboard")
                phone = st.text_input("Mobile Number")
                password = st.text_input("Password", type="password")
                
                c_1, c_2 = st.columns(2)
                with c_1:
                    if st.form_submit_button("Login 🔐", use_container_width=True):
                        u = db_login(phone, password)
                        if u:
                            st.session_state.user = u
                            st.rerun()
                        else: st.error("Invalid Credentials")
                with c_2:
                    if st.form_submit_button("Register New 📝", use_container_width=True):
                        st.session_state.auth_mode = "register"
                        st.rerun()
            
            if st.button("Forgot Password?"):
                st.session_state.auth_mode = "forgot"
                st.rerun()

        # 2. REGISTER
        elif mode == "register":
            with st.form("reg_form"):
                st.subheader("Farmer Registration")
                name = st.text_input("Full Name")
                phone = st.text_input("Mobile (10 Digits)")
                email = st.text_input("Email (For Recovery)")
                city = st.text_input("Village / City")
                dist = st.selectbox("District", ["Thanjavur", "Madurai", "Coimbatore", "Salem", "Trichy"])
                pass1 = st.text_input("Password", type="password")
                
                if st.form_submit_button("Create Account ✅", use_container_width=True):
                    if len(phone) == 10 and len(name) > 2:
                        ok, msg = db_register(name, phone, email, city, dist, pass1)
                        if ok: 
                            st.success("Registration Successful! Please Login.")
                            st.session_state.auth_mode = "login"
                            time.sleep(1)
                            st.rerun()
                        else: st.error(msg)
                    else: st.error("Invalid Details. Check Phone/Name.")
            if st.button("Back to Login"):
                st.session_state.auth_mode = "login"
                st.rerun()

        # 3. FORGOT PASSWORD
        elif mode == "forgot":
            st.subheader("Reset Password")
            email = st.text_input("Enter Registered Email")
            if st.button("Send Reset Code"):
                phone_linked = db_check_email(email)
                if phone_linked:
                    code = str(random.randint(100000, 999999))
                    st.session_state.reset_code = code
                    st.session_state.reset_email = email
                    st.session_state.reset_phone = phone_linked # Store phone to update
                    st.session_state.auth_mode = "reset"
                    st.toast(f"DEMO CODE sent to {email}: {code}", icon="📧")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Email not found in our records.")
            if st.button("Cancel"):
                st.session_state.auth_mode = "login"
                st.rerun()

        # 4. RESET VERIFICATION
        elif mode == "reset":
            st.subheader("Verify Code")
            st.info(f"Code sent to {st.session_state.reset_email}")
            user_code = st.text_input("Enter 6-digit Code")
            new_pass = st.text_input("New Password", type="password")
            
            if st.button("Update Password 🔄"):
                if user_code == st.session_state.reset_code:
                    db_update_password(st.session_state.reset_phone, new_pass)
                    st.success("Password Updated! returning to login...")
                    st.session_state.auth_mode = "login"
                    st.session_state.reset_code = None
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("Invalid Code.")

# --- SIDEBAR ---
def sidebar():
    with st.sidebar:
        st.markdown('<div class="icon-box"><span style="font-size:40px;">👨🏾‍🌾</span></div>', unsafe_allow_html=True)
        st.title("AgriAI Pro")
        st.caption("Pacha-Mann Edition")
        
        # Pongal Anim
        st.markdown("""<div style="text-align:center; margin:20px;"><span class="pongal-anim">🌾 🌞 🏺</span></div>""", unsafe_allow_html=True)
        
        st.success(f"Welcome, {st.session_state.user['name']}")
        st.caption(f"📍 {st.session_state.user['district']}")
        
        st.markdown("---")
        nav = st.radio("Menu", ["Dashboard", "Cultural Diagnosis", "Reports"])
        st.session_state.page = nav
        
        if st.button("Logout"):
            st.session_state.user = None
            st.session_state.auth_mode = "login"
            st.rerun()

# --- MAIN DASHBOARD (Simplified) ---
def main_app():
    sidebar()
    pg = st.session_state.page
    
    if pg == "Dashboard":
        st.header("Home Dashboard")
        st.markdown("### 🌤️ Weather & Advisory")
        with st.container():
            c1, c2, c3 = st.columns(3)
            c1.metric("Temperature", "32°C", "-1°C")
            c2.metric("Humidity", "65%", "Normal")
            c3.metric("Rainfall", "0mm", "Dry")
    
    elif pg == "Cultural Diagnosis":
        st.header("🌿 Cultural Diagnosis (Science + Wisdom)")
        st.info("Upload Crop Image for analysis")
        st.file_uploader("")
        st.markdown("#### Ancient Wisdom Tip:")
        st.success("During 'Agni Nakshatram', increase irrigation frequency for better root cooling.")

    elif pg == "Reports":
        st.header("📩 Farm Reports")
        st.write("Generate PDF reports for bank loans or insurance.")
        st.button("Download Monthly Summary")

# --- APP ENTRY ----------------------------------------------------------------
if not st.session_state.user:
    auth_container()
else:
    main_app()
