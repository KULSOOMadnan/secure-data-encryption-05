import streamlit as st
import hashlib
from cryptography.fernet import Fernet
import os
import json
import base64


# ----------------------------
#  Modules for Pages
# -----------------------------

from Store_data import store_data
from retrived_data import retrived_data

# -------------------------------
# 🔐 Helper Functions
# -------------------------------

def hash_passkey(passkey, salt=None):
    if not salt:
        salt = os.urandom(16)
        key = hashlib.pbkdf2_hmac(
            'sha256', passkey.encode(), salt, 100000
        )
    return base64.b64encode(salt + key).decode()


def encrypt_data(text):
    return cipher.encrypt(text.encode()).decode()


def decrypt_data(encrypted_text, passkey, label):
    hashed_passkey = hash_passkey(passkey)

    if label in st.session_state.stored_data:
        stored_entry = st.session_state.stored_data[label]

        if stored_entry["passkey"] == hashed_passkey:
            st.session_state.failed_attempts = 0
            return cipher.decrypt(encrypted_text.encode()).decode()

    st.session_state.failed_attempts += 1
    return None


def verify_passkey(stored_hash, provided_passkey):
    decoded = base64.b64decode(stored_hash.encode())
    salt = decoded[:16]
    stored_key = decoded[16:]
    new_key = hashlib.pbkdf2_hmac(
        'sha256', provided_passkey.encode(), salt, 100000
    )
    return stored_key == new_key


def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(st.session_state.stored_data, f)


# -------------------------------
# 📂 Data Persistence Setup
# -------------------------------

DATA_FILE = "store_data.json"

# Create the JSON file if it doesn't exist
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

# Load existing data into session_state
try:
    with open(DATA_FILE, "r") as f:
        loaded_data = json.load(f)
except (json.JSONDecodeError, FileNotFoundError):
    loaded_data = {}


# -------------------------------
# 🧠 Initialize Session State
# -------------------------------


# Make sure session_state matches loaded data
if "stored_data" not in st.session_state:
    st.session_state.stored_data = loaded_data

if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "locked" not in st.session_state:
    st.session_state.locked = False

if "fernet_key" not in st.session_state:
    st.session_state.fernet_key = Fernet.generate_key()

if "lockout_time" not in st.session_state:
    st.session_state.lockout_time = 0


stored_data = st.session_state.stored_data
failed_attempts = st.session_state.failed_attempts
cipher = Fernet(st.session_state.fernet_key)


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
   store_data()


# -------------------------------
# 🔍 Retrieve Data
# -------------------------------

elif page == "🔍 Retrieve Data":
    retrived_data()


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
