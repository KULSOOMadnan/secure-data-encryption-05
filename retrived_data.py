import streamlit as st
import time
from cryptography.fernet import Fernet
from utils import load_data, verify_passkey , decrypt_data


def retrived_data():
    st.title("🔍 Decrypt Stored Data")

    # ✅ Always initialize session state keys
    for key, value in {
        "failed_attempts": 0,
        "lockout_time": 0,
        "logged_in": False,
        "username": "",
        "page": "Decrypt"
    }.items():
        if key not in st.session_state:
            st.session_state[key] = value
        


    current_time = time.time()

    # 🔒 If not logged in, force to login page
    if not st.session_state.username:
        st.error("You need to login first.")
        if st.button("Go to Login"):
            st.session_state.page = '👤 Login'
            st.rerun()
        st.stop()

    # 🔒 Lockout logic
    if current_time < st.session_state.lockout_time:
        remaining = int(st.session_state.lockout_time - current_time)
        minutes, seconds = divmod(remaining, 60)
        st.error(
            f"🔒 Too many failed attempts. Locked for {minutes} min {seconds} sec.")
        st.warning("Wait before trying again.")
        st.stop()

    # ✅ Input fields for decryption
    label = st.text_input("Enter label")
    passkey = st.text_input("Enter passkey", type="password")

    if st.button("Decrypt"):
        if label and passkey:
            all_data = load_data()
            user_data = all_data.get(st.session_state.username, {})

            if label in user_data:
                encrypted_text = user_data[label]["encrypted_text"]
                stored_hash = user_data[label]["passkey"]

                if verify_passkey(stored_hash, passkey):
                    decrypted_text = decrypt_data(encrypted_text, passkey, stored_hash)
                    st.success("Secret decrypted ✅")
                    st.code(decrypted_text)
                else:
                    st.session_state.failed_attempts += 1
                    st.error("Wrong passkey ❌")
                    st.warning(
                        f"Failed Attempts: {st.session_state.failed_attempts}/3")

                    if st.session_state.failed_attempts >= 3:
                        st.session_state.lockout_time = time.time() + 180
                        st.error("🔒 Too many wrong attempts. Redirecting you to login page in 3 seconds...")
                        with st.spinner("Redirecting..."):
                            time.sleep(3)
                        st.session_state.page = '👤 Login'
                        st.rerun()

            else:
                st.error("Label not found.")
        else:
            st.warning("Enter both fields.")


if __name__ == "__main__":
    retrived_data()
