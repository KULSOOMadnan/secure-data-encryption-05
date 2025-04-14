import streamlit as st
import hashlib
from cryptography.fernet import Fernet
import os
import json
import base64

cipher = Fernet(st.session_state.fernet_key)


def hash_passkey(passkey):
    key = hashlib.pbkdf2_hmac(
        'sha256', passkey.encode(), b'', 100000
    )
    return base64.b64encode(key).decode()


def encrypt_data(text):

    return cipher.encrypt(text.encode()).decode()


def decrypt_data(encrypted_text, passkey, stored_hash):

    if verify_passkey(stored_hash, passkey):
        st.session_state.failed_attempts = 0
        try:
            # Check the encrypted text
            print("Attempting to decrypt:", encrypted_text)
            decrypted_text = cipher.decrypt(
                encrypted_text.encode()).decode()  # Decrypt the text
            return decrypted_text
        except Exception as e:
            print(
                f"Decryption failed: {e}. This usually means the encrypted text or passkey is incorrect!")
            return None


def verify_passkey(stored_hash, provided_passkey):
    return stored_hash == hash_passkey(provided_passkey)


DATA_FILE = "store_data.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({}, f)
        return {}

    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        with open(DATA_FILE, "w") as f:
            json.dump({}, f)
        return {}


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


# import streamlit as st
# import hashlib
# from cryptography.fernet import Fernet
# import os
# import json
# import base64

# # -------------------------------
# # 🔐 Helper Functions
# # -------------------------------


# def hash_passkey(passkey, salt=None):
#     if not salt:
#         salt = os.urandom(16)
#         key = hashlib.pbkdf2_hmac(
#             'sha256', passkey.encode(), salt, 100000
#         )
#     return base64.b64encode(salt + key).decode()


# def encrypt_data(text):
#     cipher = Fernet(st.session_state.fernet_key)
#     return cipher.encrypt(text.encode()).decode()


# def decrypt_data(encrypted_text, passkey, label):
#     cipher = Fernet(st.session_state.fernet_key)
#     if label in st.session_state.stored_data:
#         stored_entry = st.session_state.stored_data[label]

#         if verify_passkey(stored_entry["passkey"], passkey):
#             st.session_state.failed_attempts = 0
#             return cipher.decrypt(encrypted_text.encode()).decode()

#     st.session_state.failed_attempts += 1
#     return None


# def verify_passkey(stored_hash, provided_passkey):
#     decoded = base64.b64decode(stored_hash.encode())
#     salt = decoded[:16]
#     stored_key = decoded[16:]
#     new_key = hashlib.pbkdf2_hmac(
#         'sha256', provided_passkey.encode(), salt, 100000
#     )
#     return stored_key == new_key


# # -------------------------------
# # 📂 Data Persistence Setup
# # -------------------------------

# DATA_FILE = "store_data.json"

# def load_data():
#     if not os.path.exists(DATA_FILE):
#         with open(DATA_FILE, "w") as f:
#             json.dump({}, f)
#         return {}

#     try:
#         with open(DATA_FILE, "r") as f:
#             return json.load(f)
#     except (json.JSONDecodeError, FileNotFoundError):
#         # If file's corrupted or missing — reset it
#         with open(DATA_FILE, "w") as f:
#             json.dump({}, f)
#         return {}

# def save_data(data):
#     with open(DATA_FILE, "w") as f:
#         json.dump(data, f, indent=4)


# if "stored_data" not in st.session_state:
#     st.session_state.stored_data = load_data()

# if "fernet_key" not in st.session_state:
#     st.session_state.fernet_key = Fernet.generate_key()
