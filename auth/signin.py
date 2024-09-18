import streamlit as st
import sqlite3
import hashlib

def signin():
    st.subheader("Sign In")

    with st.form(key="signin_form", clear_on_submit=True):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Sign In")

    if submit_button:
        print("Sign In button clicked")  # Debug print
        conn = sqlite3.connect('mydatabase.db')
        cursor = conn.cursor()
        
        # hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        cursor.execute("SELECT * FROM Users WHERE user_email = ? AND user_password = ?", (email, password))
        result = cursor.fetchone()
        print(result)
        if result:
            print("Login successful")  # Debug print
            st.session_state.user_id = result[0]
            st.success("Logged in successfully!")
            st.rerun()
        else:
            print("Invalid email or password")  # Debug print
            st.error("Invalid email or password!")
        
        conn.close()

    print("End of signin function")  # Debug print


    