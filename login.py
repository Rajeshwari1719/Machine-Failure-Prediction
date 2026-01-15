import streamlit as st
import hashlib
import pandas as pd

# --- Helper Functions ---
def hash_password(password):
    """Hash a password for storing."""
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(password, hashed):
    """Check hashed password."""
    return hash_password(password) == hashed

# --- Load or Initialize Users Database ---
if 'users_db' not in st.session_state:
    st.session_state['users_db'] = pd.DataFrame(columns=['username', 'password'])

# --- Main App ---
st.title("🔐 Login / Sign Up Page")

menu = ["Login", "Sign Up"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Sign Up":
    st.subheader("Create a new account")
    new_user = st.text_input("Username")
    new_password = st.text_input("Password", type='password')
    
    if st.button("Sign Up"):
        if new_user in st.session_state['users_db']['username'].values:
            st.error("Username already exists. Try another.")
        elif new_user == "" or new_password == "":
            st.error("Please enter both username and password.")
        else:
            # Save hashed password
            hashed_pw = hash_password(new_password)
            st.session_state['users_db'] = st.session_state['users_db'].append(
                {'username': new_user, 'password': hashed_pw}, ignore_index=True
            )
            st.success("Account created successfully! Go to Login menu.")

elif choice == "Login":
    st.subheader("Login with your account")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    
    if st.button("Login"):
        user_row = st.session_state['users_db'][st.session_state['users_db']['username'] == username]
        if not user_row.empty:
            stored_password = user_row['password'].values[0]
            if check_password(password, stored_password):
                st.success(f"Welcome, {username}!")
                # You can add your main app page here
                st.write("This is your dashboard or main page.")
            else:
                st.error("Incorrect password.")
        else:
            st.error("User not found. Please Sign Up first.")
