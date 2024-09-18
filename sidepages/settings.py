import streamlit as st
import sqlite3

def show_settings():
    st.header("Settings")
    st.write("Here you can manage your account settings and secrets.")

    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    # Display existing secrets
    st.subheader("Your Secrets")
    cursor.execute("SELECT secret_id, secret_name, secret_value FROM Secrets WHERE user_id = ?", (st.session_state.user_id,))
    secrets = cursor.fetchall()

    if secrets:
        for secret in secrets:
            with st.expander(f"Secret: {secret[1]}"):
                with st.form(key=f'edit_secret_form_{secret[0]}'):
                    edited_name = st.text_input("Secret Name", value=secret[1])
                    edited_value = st.text_input("Secret Value", value=secret[2], type="password")
                    col1, col2 = st.columns(2)
                    with col1:
                        update_button = st.form_submit_button("Update Secret")
                    with col2:
                        delete_button = st.form_submit_button("Delete Secret")

                    if update_button:
                        if edited_name and edited_value:
                            cursor.execute("UPDATE Secrets SET secret_name = ?, secret_value = ? WHERE secret_id = ?",
                                           (edited_name, edited_value, secret[0]))
                            conn.commit()
                            st.success("Secret updated successfully!")
                            st.rerun()
                        else:
                            st.error("Please enter both secret name and value.")
                    
                    if delete_button:
                        cursor.execute("DELETE FROM Secrets WHERE secret_id = ?", (secret[0],))
                        conn.commit()
                        st.success("Secret deleted successfully!")
                        st.rerun()
    else:
        st.info("You don't have any secrets stored yet.")

    # Add New Secret button
    if st.button("Add New +"):
        st.session_state.show_new_secret_form = True

    # Show New Secret form
    if st.session_state.get('show_new_secret_form', False):
        with st.form(key='add_secret_form'):
            st.subheader("Add New Secret")
            secret_name = st.text_input("Secret Name")
            secret_value = st.text_input("Secret Value", type="password")
            submit_button = st.form_submit_button("Save Secret")

            if submit_button:
                if secret_name and secret_value:
                    cursor.execute("INSERT INTO Secrets (user_id, secret_name, secret_value) VALUES (?, ?, ?)",
                                   (st.session_state.user_id, secret_name, secret_value))
                    conn.commit()
                    st.success("Secret saved successfully!")
                    st.session_state.show_new_secret_form = False
                    st.rerun()
                else:
                    st.error("Please enter both secret name and value.")

    conn.close()

    # Placeholder for future functionality
    st.info("Additional account settings and preferences will be available here in future updates.")

# Initialize session state
if 'show_new_secret_form' not in st.session_state:
    st.session_state.show_new_secret_form = False


    