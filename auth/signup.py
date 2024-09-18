import streamlit as st
import sqlite3
from streamlit_extras.row import row

def create_user(email, password):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Users (user_email, user_password) VALUES (?, ?)", (email, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def signup():
    st.title("Sign Up")

    with st.form(key="signup_form", clear_on_submit=True):
        st.subheader("Sign Up") 
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        links_row = row(2, vertical_align="center")
        submitted = links_row.form_submit_button(
            "📖  Sign Up",
            use_container_width = True
            )

        if submitted:
            if password != confirm_password:
                st.error("Passwords do not match!")
            else:
                if create_user(email, password):
                    st.success("Your account has been successfully created! You can now log in.")
                else:
                    st.error("Email already exists. Please use a different email.")

            
if __name__ == "__main__":
    signup()


    