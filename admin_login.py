import streamlit as st

def admin_login ():
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
if __name__ == "__main__":
    admin_login()