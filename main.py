import streamlit as st
from cryptography.fernet import Fernet
import hashlib
import os
import json
import time

# ----------------------------
#  Modules for Pages
# -----------------------------

import Store_data
import retrived_data
import admin_login
from utils import load_data
from auth_utils import save_session
import home
# -------------------------------
# 🧠 Initialize Session State
# -------------------------------
if "username" not in st.session_state:
    st.session_state.username = ''
if "page" not in st.session_state:
    st.session_state.page = "👤 Sign Up"
if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

def logout():
    if os.path.exists("session.json"):
        os.remove("session.json")
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.page = "👤 Login"
    st.rerun()



def load_session():
    if os.path.exists("session.json"):
        with open("session.json", "r") as f:
            return json.load(f)
    return None


# Load session on startup
session_data = load_session()

if session_data:
    st.session_state.logged_in = session_data.get("logged_in", False)
    st.session_state.username = session_data.get("username", "")
else:
    st.session_state.logged_in = False
    st.session_state.username = ""


# -------------------------------
# 🧭 Sidebar Navigation
# -------------------------------

if st.session_state.username:
    initial = st.session_state.username[0].upper()
    st.sidebar.markdown(f"""
        <div style="display:flex;align-items:center;gap:10px;">
            <div style="
                background-color:#4CAF50;
                color:white;
                width:50px;
                height:50px;
                border-radius:50%;
                display:flex;
                align-items:center;
                justify-content:center;
                font-size:18px;
                font-weight:bold;
                border:2px solid #2E7D32;
                ">
                {initial}
            </div>
            <span style="font-size:16px;"><b>{st.session_state.username}</b></span>
        </div>
    """, unsafe_allow_html=True)



    
st.sidebar.title('Secure Vault')

selected_page = st.sidebar.radio(
    "Navigate",
    ["👤 Sign Up", "👤 Login", "🏠 Home", "📦 Store Data",
        "🔍 Retrieve Data", "🔑 Admin Login", "📋 Stored Labels"],
    index=["👤 Sign Up", "👤 Login", "🏠 Home", "📦 Store Data", "🔍 Retrieve Data",
           "🔑 Admin Login", "📋 Stored Labels"].index(st.session_state.page)
)

if selected_page != st.session_state.page:
    st.session_state.page = selected_page
    st.rerun()  # re-run the app immediately with new page

if st.session_state.username and  st.sidebar.button("Logout"):
        logout()




# -------------------------------
# 🏠 Home Page
# -------------------------------

if st.session_state.page == "🏠 Home":
    home.home()

# -------------------------------
# 👤 Sign Up Page
# -------------------------------

elif st.session_state.page == "👤 Sign Up":
    from auth_utils import signup, login

    st.title("👤 User Sign Up")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button('Signup'):
        if username and password:
            success, message = signup(username, password, confirm_password)
            if success:
                st.success(message)
                st.session_state.page = "👤 Login"
                st.rerun()   # clean modern way
            else:
                st.error(message)

        else:
            st.warning("Please enter both username and password")

# -------------------------------
# 👤 Login  Page
# -------------------------------

elif st.session_state.page == "👤 Login":
    from auth_utils import login
    st.title("👤 User Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button('Login'):
        success, message = login(username, password)
        if success:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Welcome back {username} 🔓")
            st.success("Logged in successfully ✅")
            time.sleep(1)
            save_session(username)  # 👈 new line
            st.session_state.page = "🏠 Home"
            st.rerun()   # clean modern way

        else:
            st.error(message)
    else:
        st.warning("Please enter both username and password")

# -------------------------------
# 📋 Stored Labels
# -----------------------
elif st.session_state.page == '📋 Stored Labels':
    st.subheader("📋 Stored Labels")

    if not st.session_state.username:
        st.error("You need to login first.")
        st.stop()

    # Load fresh data from JSON
    all_data = load_data()

    # Get current user's stored data
    user_data = all_data.get(st.session_state.username, {})

    if user_data:
        st.success(f"Secrets stored for {st.session_state.username}:")
        for label in user_data.keys():
            st.write(f"🔐 {label}")
    else:
        st.info("No secrets stored yet.")

# -------------------------------
# 🔑Admin Login
# -------------------------------

elif st.session_state.page == "🔑 Admin Login":
    admin_login.admin_login()


# -------------------------------
# 📦 Store Data
# -------------------------------

elif st.session_state.page == "📦 Store Data":
    Store_data.store_data()


# -------------------------------
# 🔍 Retrieve Data
# -------------------------------

elif st.session_state.page == "🔍 Retrieve Data":
    retrived_data.retrived_data()
