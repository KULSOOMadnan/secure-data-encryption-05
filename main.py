import streamlit as st
import hashlib
from cryptography.fernet import Fernet
import os
import json
import base64


# ----------------------------
#  Modules for Pages
# -----------------------------

import Store_data 
import retrived_data 


# -------------------------------
# 🧭 Sidebar Navigation
# -------------------------------
st.sidebar.title('Secure Vault')
page = st.sidebar.radio(
    "Navigate", ["🏠 Home", "📦 Store Data", "🔍 Retrieve Data", "🔑 Admin Login", '📋 Stored Labels'])

# Show login status on all pages
if st.session_state.logged_in:
    st.sidebar.success("✅ Logged in as Admin")
else:
    st.sidebar.warning("🔒 Not Logged In")

# -------------------------------
# 🏠 Home Page
# -------------------------------

if page == "🏠 Home":
    st.title("🔒 Secure Data Encryption System")
    st.write("""
    - Store & protect sensitive data
    - Unlock secrets with passkey
    - 3 wrong attempts = LOCK
    - Login any time to unlock 🔓
    """)

# -------------------------------
# 📦 Store Data
# -------------------------------

elif page == "📦 Store Data":
   Store_data.store_data()


# -------------------------------
# 🔍 Retrieve Data
# -------------------------------

elif page == "🔍 Retrieve Data":
    retrived_data.retrived_data()


# -------------------------------
# 📋 Stored Labels
# -------------------------------
elif page == '📋 Stored Labels':

    st.subheader("📋 Stored Labels")
    if st.session_state.stored_data:
        for label in st.session_state.stored_data.keys():
            st.write(f"- {label}")
    else:
        st.write("No secrets stored yet.")

# -------------------------------
# 🔑 Login Page (Now in Sidebar)
# -------------------------------

elif page == "🔑 Admin Login":
    st.title("🔑 Admin Login")
    login_user = st.text_input("Enter user name : ")
    login_pw = st.text_input("Enter admin password:", type="password")

    if st.button("Login"):
        if login_pw == "admin123":
            st.session_state.logged_in = True
            st.session_state.failed_attempts = 0
            st.session_state.lockout_time = 0

            st.success(f"{login_user}, You're in, boss! 🔓")
            st.success(
                "✅ Reauthorized successfully! Redirecting to Retrieve Data...")
        else:
            st.error("Wrong password")
