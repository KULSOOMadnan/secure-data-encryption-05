import streamlit as st
from utils import encrypt_data , hash_passkey , save_data

def store_data():

    st.title("📦 Encrypt & Store")
    label = st.text_input("Label for your secret")
    data = st.text_area("Enter Encrypted Data:")
    passkey = st.text_input("Set a passkey", type="password")

    if st.button("Encrypt & Save"):
        if label and data and passkey:
            encrypted = encrypt_data(data)
            st.session_state.stored_data[label] = {
                "encrypted_text": encrypted,
                "passkey": hash_passkey(passkey),

            }
            save_data()
            st.success(f"Stored under: {label}")
            st.code(encrypted)
        else:
            st.warning("All fields required")
            
            
if __name__ == "__main__":
    store_data()