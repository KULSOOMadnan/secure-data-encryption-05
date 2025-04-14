import hashlib
import json
import os

USERS_FILE = "users.json"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    # Check if file exists — if not, create it with empty JSON object
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)
        return {}

    # If file exists but is empty or invalid JSON — handle gracefully
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        # Reinitialize file with empty JSON if corrupted
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)
        return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def signup(username, password, confirm_pass):
    users = load_users()
    if username in users:
        return False, "Username already exists"
    if password != confirm_pass:
        return False, "Confirm Password doesn't match"
    users[username] = hash_password(confirm_pass)
    save_users(users)
    return True, "Signup successful"

def login(username, password):
    users = load_users()
    if username in users and users[username] == hash_password(password):
        return True, "Login successful"
    return False, "Invalid credentials"

def save_session(username):
    session_data = {"username": username, "logged_in": True}
    with open("session.json", "w") as f:
        json.dump(session_data, f)


