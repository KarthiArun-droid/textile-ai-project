import streamlit as st
import hashlib
from database.db import cursor, conn

# -------------------------
# PASSWORD HASHING
# -------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# -------------------------
# REGISTER
# -------------------------
def register_user(username, email, password):
    try:
        hashed = hash_password(password)

        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (username, email, hashed)
        )
        conn.commit()
        return True
    except:
        return False

# -------------------------
# LOGIN
# -------------------------
def login_user(username, password):
    hashed = hash_password(password)

    cursor.execute(
        "SELECT id, username, role FROM users WHERE username=? AND password=?",
        (username, hashed)
    )
    return cursor.fetchone()

# -------------------------
# FORGOT PASSWORD
# -------------------------
def reset_password(email, new_password):
    hashed = hash_password(new_password)

    cursor.execute(
        "UPDATE users SET password=? WHERE email=?",
        (hashed, email)
    )
    conn.commit()

# -------------------------
# LOGIN SCREEN
# -------------------------
def login_screen():

    st.title("🔐 TextileAI Login System")

    tab1, tab2, tab3 = st.tabs(["Login", "Register", "Forgot Password"])

    # LOGIN
    with tab1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            user = login_user(username, password)

            if user:
                st.session_state.logged_in = True
                st.session_state.user_id = user[0]
                st.session_state.username = user[1]
                st.session_state.role = user[2]
                st.success("Login Successful")
                st.rerun()
            else:
                st.error("Invalid Credentials")

    # REGISTER
    with tab2:
        new_user = st.text_input("Create Username")
        email = st.text_input("Email")
        new_pass = st.text_input("Create Password", type="password")

        if st.button("Register"):
            if register_user(new_user, email, new_pass):
                st.success("Account Created Successfully")
            else:
                st.error("Username or Email already exists")

    # FORGOT PASSWORD
    with tab3:
        email = st.text_input("Enter Registered Email")
        new_pass = st.text_input("New Password", type="password")

        if st.button("Reset Password"):
            reset_password(email, new_pass)
            st.success("Password Updated Successfully")

    st.stop()