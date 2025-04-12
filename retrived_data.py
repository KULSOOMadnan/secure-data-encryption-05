import streamlit as st 
from cryptography.fernet import Fernet
import time
from utils import stored_data , verify_passkey

def retrived_data():
    st.title("🔍 Decrypt Stored Data")

    current_time = time.time()

    # Check for lockout
    if current_time < st.session_state.lockout_time and not st.session_state.logged_in:
        remaining = int(st.session_state.lockout_time - current_time)
        minutes, seconds = divmod(remaining, 60)
        st.error(
            f"🔒 Too many failed attempts. Locked for {minutes} min {seconds} sec.")
        st.warning("⚠️ Redirect to Admin Login required to unlock.")
        st.stop()

    label = st.text_input("Enter label")
    passkey = st.text_input("Enter passkey", type="password")

    if st.button("Decrypt"):
        if label and passkey:
            if label in stored_data:
                encrypted_text = stored_data[label]["encrypted_text"]
                stored_hash = stored_data[label]["passkey"]

                if verify_passkey(stored_hash, passkey):
                    try:
                        cipher = Fernet(st.session_state.fernet_key)
                        decrypted_text = cipher.decrypt(
                            encrypted_text.encode()).decode()
                        st.success("Secret decrypted ✅")
                        st.code(decrypted_text)
                        st.session_state.failed_attempts = 0
                    except Exception as e:
                        st.error("Decryption failed — invalid token.")
                        st.warning(
                            "Possible data/key mismatch. Contact admin.")
                else:
                    st.session_state.failed_attempts += 1
                    st.error("Wrong passkey ❌")
                    st.warning(
                        f"Failed Attempts: {st.session_state.failed_attempts}/3")

                    if st.session_state.failed_attempts >= 3:
                        st.session_state.lockout_time = time.time() + 180
                        st.error("🔒 Locked out due to too many wrong attempts!")
            else:
                st.error("Label not found")
        else:
            st.warning("Enter both fields")
            
if __name__ == "__main__":
    retrived_data()