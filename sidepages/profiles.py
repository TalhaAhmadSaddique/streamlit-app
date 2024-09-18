import streamlit as st
import sqlite3

def show_profiles():
    st.subheader("Your Profiles")

    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    cursor.execute("SELECT profile_id, profile_title, profile_description FROM Profiles WHERE user_id = ?", (st.session_state.user_id,))
    profiles = cursor.fetchall()

    if profiles:
        for profile in profiles:
            with st.expander(f"Profile: {profile[1]}"):
                with st.form(key=f'edit_profile_form_{profile[0]}'):
                    edited_title = st.text_input("Profile Title", value=profile[1])
                    edited_description = st.text_area("Profile Description", value=profile[2])
                    col1, col2 = st.columns(2)
                    with col1:
                        update_button = st.form_submit_button("Update Profile")
                    with col2:
                        delete_button = st.form_submit_button("Delete Profile")

                    if update_button:
                        if edited_title and edited_description:
                            cursor.execute("UPDATE Profiles SET profile_title = ?, profile_description = ? WHERE profile_id = ?",
                                           (edited_title, edited_description, profile[0]))
                            conn.commit()
                            st.success("Profile updated successfully!")
                            st.rerun()
                        else:
                            st.error("Please enter both profile title and description.")
                    
                    if delete_button:
                        cursor.execute("DELETE FROM Profiles WHERE profile_id = ?", (profile[0],))
                        conn.commit()
                        st.success("Profile deleted successfully!")
                        st.rerun()
    else:
        st.info("You don't have any profiles yet.")

    # Add New Profile button
    if st.button("Add New +"):
        st.session_state.show_new_profile_form = True

    # Show New Profile form
    if st.session_state.get('show_new_profile_form', False):
        with st.form(key='add_profile_form'):
            st.subheader("Create New Profile")
            new_profile_title = st.text_input("New Profile Title")
            new_profile_description = st.text_area("New Profile Description")
            submit_button = st.form_submit_button("Save New Profile")

            if submit_button:
                if new_profile_title and new_profile_description:
                    cursor.execute("INSERT INTO Profiles (user_id, profile_title, profile_description) VALUES (?, ?, ?)",
                                   (st.session_state.user_id, new_profile_title, new_profile_description))
                    conn.commit()
                    st.success("New profile created successfully!")
                    st.session_state.show_new_profile_form = False
                    st.rerun()
                else:
                    st.error("Please enter both profile title and description.")

    conn.close()

# Initialize session state
if 'show_new_profile_form' not in st.session_state:
    st.session_state.show_new_profile_form = False


    