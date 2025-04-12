import streamlit as st
from auth_utils import signup, login

# Session state to track logged-in user
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

st.title("🔒 Secure Data System — Login / Sign Up")

# Option to switch between login and signup
page = st.sidebar.selectbox("Choose Option", ["Login", "Sign Up"])

if page == "Sign Up":
    st.subheader("Create New Account")

    new_username = st.text_input("Choose a Username")
    new_password = st.text_input("Choose a Password", type="password")
    if st.button("Sign Up"):
        if new_username == "" or new_password == "":
            st.error("Bruh, fill both fields!")
        else:
            success, message = signup(new_username, new_password)
            if success:
                st.success(message)
                st.info("Go to Login page now.")
            else:
                st.error(message)

elif page == "Login":
    st.subheader("Login to Your Account")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "" or password == "":
            st.error("Yo, fill both fields!")
        else:
            success, message = login(username, password)
            if success:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome back, {username}!")
                st.rerun()  # reload to show main app
            else:
                st.error(message)

# After login show rest of the app
if st.session_state.logged_in:
    st.sidebar.success(f"Logged in as: {st.session_state.username}")
    st.write("✅ Now you can add / retrieve your encrypted data here bro!")

    # Here we’ll call Phase 2/3 features next 👌
    
