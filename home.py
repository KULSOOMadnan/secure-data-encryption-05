import streamlit as st

def home():
    st.title("🔐 Secure Data Encryption System")

    st.markdown("""
    ## 📖 Application Overview  

    Welcome to my **Secure Data Encryption System** — a privacy-focused application built with **Python** and **Streamlit** for my assignment project. This system allows multiple users to securely encrypt and store secret data, retrieve it later, and safely manage their information with passkey protection.  

    The application uses **Fernet symmetric encryption** for data protection, **JSON-based local storage**, and **session state management** to maintain user authentication, track login attempts, and prevent unauthorized access.

    ---

    ## 📑 Application Pages & Features  

    Here's a breakdown of each page you can access through the radio button menu on the sidebar:

    ### 🏠 Home  
    This page you're currently on — it provides a complete overview of the application, its purpose, technology used, and explanations of all available pages.

    ### 👤 Login  
    - Allows a user to **enter their username** and **decrypt the Fernet key** associated with their session.
    - If no valid username is provided, access to other pages is restricted.
    - Session state stores the `username` and encryption key after login.

    ### 📝 Add Secret Data  
    - Users can **enter a label** (like "email password" or "bank PIN"), **write the secret text**, and **set a custom passkey** for decryption later.
    - Data is encrypted using Fernet and saved in a **local JSON file** with the encrypted text and a hashed version of the passkey.
    - Multiple records can be saved per user.

    ### 🔍 Decrypt Stored Data  
    - Users can **retrieve previously saved encrypted text** by entering the corresponding label and the passkey they set earlier.
    - If the passkey matches the stored hash:
      - The encrypted text is decrypted and displayed.
    - If the passkey is incorrect:
      - The number of failed attempts increments.
      - After **3 failed attempts**, the user is **locked out for 3 minutes**.
      - During lockout:
        - The input fields are disabled.
        - A countdown timer shows remaining lockout time.
        - The user is redirected to the **Login** page after lockout.
    - Session state manages failed attempts and lockout timing.

    ### 🚪 Logout  
    - Ends the user's session by clearing all relevant session states.
    - Redirects the user back to the **Login** page.
    - Ensures no leftover session data remains for security.

    ---

    ## 🔐 Security Features  
    - **Fernet Encryption**: All secret texts are encrypted before storage.
    - **Passkey Hashing**: Passkeys aren’t stored in plain text — only their hashed version is saved.
    - **Session Management**: Streamlit's `session_state` tracks user logins, encryption keys, failed attempts, and lockout durations.
    - **Failed Attempt Lockout**: 3 wrong attempts trigger a 3-minute lockout, during which users can’t access decryption functions.

    ---

    ## 📊 Tech Stack  
    - **Python**
    - **Streamlit**
    - **cryptography (Fernet)**
    - **Local JSON storage**
    - **Streamlit `session_state`**

    ---

    ## 📌 Assignment Purpose  
    This project was built to demonstrate secure encryption, user authentication, state management, and access control features in a web application environment using **Streamlit**.

    It showcases:
    - Symmetric encryption handling
    - Passkey-based data protection
    - Session-based user-specific data access
    - Temporary lockout mechanisms for enhanced security

    ---

    🔒 **Your secrets stay yours. No one sees them without your passkey.**

    """)

if __name__ == "__main__":
    home()
