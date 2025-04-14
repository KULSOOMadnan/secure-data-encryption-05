import streamlit as st
from utils import encrypt_data, hash_passkey, load_data, save_data

def store_data():
    st.title("📦 Encrypt & Store")

    if not st.session_state.username:
        st.error("You need to login first.")
        st.stop()

    st.write(f"Logged in as: {st.session_state.username}")  # temp debug line

    label = st.text_input("Label for your secret")
    data = st.text_area("Enter data to encrypt:")
    passkey = st.text_input("Set a passkey", type="password")

    if st.button("Encrypt & Save"):
        if label and data and passkey:
            all_data = load_data()

            # Fetch user's existing data or empty dict
            user_data = all_data.get(st.session_state.username, {})

            # Encrypt and add new data
            encrypted = encrypt_data(data)
            user_data[label] = {
                "encrypted_text": encrypted,
                "passkey": hash_passkey(passkey),
            }

            # Save it back
            all_data[st.session_state.username] = user_data
            save_data(all_data)

            st.success(f"Stored under: {label}")
            st.code(encrypted)
        else:
            st.warning("All fields required")

if __name__ == "__main__":
    store_data()
