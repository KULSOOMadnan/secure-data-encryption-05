from cryptography.fernet import Fernet
import json
import os

key = Fernet.generate_key()
fernet = Fernet(key)

def load_data():
    if not os.path.exists("data.json"):
        with open("data.json", "w") as f:
            json.dump({"users": {}}, f)
    with open("data.json", "r") as f:
        return json.load(f)

def save_data(data):
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)

def signup(username, password):
    data = load_data()
    if username in data["users"]:
        return False, "User already exists."
    encrypted_password = fernet.encrypt(password.encode()).decode()
    data["users"][username] = {"password": encrypted_password, "data": []}
    save_data(data)
    return True, "Signup successful."

def login(username, password):
    data = load_data()
    if username not in data["users"]:
        return False, "User not found."
    stored_password = data["users"][username]["password"]
    if fernet.decrypt(stored_password.encode()).decode() == password:
        return True, "Login successful."
    else:
        return False, "Incorrect password."
