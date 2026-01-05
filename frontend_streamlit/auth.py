import sqlite3
import hashlib

DB_PATH = "agri_pro.db"

def init_db():
    """Initializes the SQLite database with the users table."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    name TEXT NOT NULL, 
                    phone TEXT UNIQUE NOT NULL,
                    email TEXT, 
                    city TEXT NOT NULL, 
                    district TEXT NOT NULL, 
                    password_hash TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

def hash_password(password):
    """Hashes a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def login_user(phone, password):
    """
    Authenticates a user.
    Returns user dict if successful, None otherwise.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE phone = ? AND password_hash = ?", (phone, hash_password(password)))
    user = c.fetchone()
    conn.close()
    if user:
        return {
            "id": user[0],
            "name": user[1],
            "phone": user[2],
            "email": user[3],
            "city": user[4],
            "district": user[5]
        }
    return None

def register_user(name, phone, email, city, district, password):
    """
    Registers a new user.
    Returns (Success: bool, Message: str).
    """
    if len(phone) != 10 or not phone.isdigit():
        return False, "Invalid Phone Number (Must be 10 digits)"
    
    if len(password) < 4:
        return False, "Password too short (Min 4 chars)"

    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO users (name, phone, email, city, district, password_hash) VALUES (?, ?, ?, ?, ?, ?)",
                  (name, phone, email, city, district, hash_password(password)))
        conn.commit()
        conn.close()
        return True, "Registration Successful"
    except sqlite3.IntegrityError:
        return False, "Phone Number already registered"
    except Exception as e:
        return False, f"Error: {str(e)}"

def check_email_exists(email):
    """Checks if an email exists in the DB for password recovery."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT phone FROM users WHERE email = ?", (email,))
    user = c.fetchone()
    conn.close()
    return user[0] if user else None


import smtplib
from email.message import EmailMessage
import streamlit as st
import random

def send_otp_email(to_email):
    """
    Sends a 4-digit OTP to the user's email.
    Returns (OTP, None) if successful, (None, error_msg) otherwise.
    """
    otp = str(random.randint(1000, 9999))
    
    try:
        # Try finding credentials in secrets.toml first (Local), then Environment Variables (Render)
        if "email" in st.secrets:
             email_user = st.secrets["email"]["email_user"]
             email_pass = st.secrets["email"]["email_password"]
        else:
             import os
             email_user = os.getenv("EMAIL_USER")
             email_pass = os.getenv("EMAIL_PASSWORD")
             
        if not email_user or not email_pass:
            return None, "Email credentials not configured on server."

        # Strip spaces just in case
        email_pass = email_pass.replace(" ", "")
        
        msg = EmailMessage()
        msg.set_content(f"🌾 AgriAI Password Reset\n\nYour OTP is: {otp}\n\nplease do not share this code.")
        msg['Subject'] = 'AgriAI Reset Code'
        msg['From'] = email_user
        msg['To'] = to_email
        
        # Gmail SMTP - using SMTP_SSL for port 465
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_user, email_pass)
            smtp.send_message(msg)
            
        return otp, None
    except Exception as e:
        print(f"Email Error: {e}")
        return None, str(e)

def update_password(phone, new_password):
    """Updates the password for a given phone number."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE users SET password_hash = ? WHERE phone = ?", (hash_password(new_password), phone))
    conn.commit()
    conn.close()

