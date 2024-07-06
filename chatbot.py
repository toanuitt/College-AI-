import streamlit as st
import yaml
from passlib.hash import pbkdf2_sha256
import random
import string
from app import home,search_semantic

# Load configuration from YAML file
with open('config.yaml') as file:
    config = yaml.safe_load(file)

# Check if 'users' key exists in the configuration, if not, create an empty dictionary
if 'users' not in config:
    config['users'] = {}

# Initialize session state
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# Function to save the configuration to the YAML file
def save_config():
    with open('config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)

def main():
    st.title("College AI Advisor")

    menu = ["Login", "Home","Search", "Register", "Change Password", "Forgot Password", "Logout"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home Page")
        if st.session_state.current_user:
            st.subheader("Welcome ",st.session_state.current_user)
            home()
        else:
            st.warning("Please login to use the function")   
    elif choice == "Login":
        if st.session_state.current_user:
            st.write("You has successfully signed in")
        else:
            login()
    elif choice == "Search":
        if st.session_state.current_user:
            search_semantic()
        else:
            st.warning("Please login to use the function") 
    elif choice == "Register":
        if st.session_state.current_user:
            st.warning("Please log out before registering")
        else:
            register()
    elif choice == "Change Password":
        if st.session_state.current_user:
            change_password()
        else:
            st.warning("Please login to change password.")
    elif choice == "Forgot Password":
        forgot_password()
    elif choice == "Logout":
        if st.session_state.current_user:
            logout()
        else:
            st.warning("You are not in any account")
       

def login():
    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        st.session_state.current_user = login_user(username, password)

def register():
    st.subheader("Register")

    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        register_user(new_username, new_password)

def change_password():
    st.subheader("Change Password")

    current_password = st.text_input("Current Password", type="password")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm New Password", type="password")

    if st.button("Change Password"):
        change_password_user(st.session_state.current_user, current_password, new_password)

def forgot_password():
    st.subheader("Forgot Password")

    username = st.text_input("Username")

    if st.button("Reset Password"):
        reset_password(username)

def logout():
    st.session_state.current_user = None
    st.write("Your account has exited")

def login_user(username, password):
    if username in config['users']:
        stored_password = config['users'][username]['password']
        if pbkdf2_sha256.verify(password, stored_password):
            st.success("Logged in as {}".format(username))
            return username
        else:
            st.error("Incorrect password.")
    else:
        st.error("User does not exist.")

def register_user(username, password):
    if username not in config['users']:
        hashed_password = pbkdf2_sha256.hash(password)
        config['users'][username] = {'password': hashed_password}
        save_config()
        st.success("Registered successfully. You can now login.")
    else:
        st.warning("Username already exists. Choose a different username.")

def change_password_user(username, current_password, new_password):
    if username in config['users']:
        stored_password = config['users'][username]['password']
        if pbkdf2_sha256.verify(current_password, stored_password):
            hashed_new_password = pbkdf2_sha256.hash(new_password)
            config['users'][username]['password'] = hashed_new_password
            save_config()
            st.success("Password changed successfully.")
        else:
            st.error("Incorrect current password.")
    else:
        st.error("User does not exist.")

def reset_password(username):
    if username in config['users']:
        new_password = generate_random_password()
        hashed_new_password = pbkdf2_sha256.hash(new_password)
        config['users'][username]['password'] = hashed_new_password
        save_config()
        st.success("Password reset successfully. New password: {}".format(new_password))
    else:
        st.error("User does not exist.")

def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choice(characters) for i in range(length))


if __name__ == "__main__":
    main()
