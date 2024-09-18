import streamlit as st
import sqlite3

def show_portfolios():
    st.subheader("Your Portfolios")

    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    cursor.execute("SELECT portfolio_id, project_title, project_description, project_tech_stack FROM Portfolios WHERE user_id = ?", (st.session_state.user_id,))
    portfolios = cursor.fetchall()

    if portfolios:
        for portfolio in portfolios:
            with st.expander(f"Project: {portfolio[1]}"):
                with st.form(key=f'edit_portfolio_form_{portfolio[0]}'):
                    edited_title = st.text_input("Project Title", value=portfolio[1])
                    edited_description = st.text_area("Project Description", value=portfolio[2])
                    edited_tech_stack = st.text_input("Technologies (comma-separated)", value=portfolio[3])
                    col1, col2 = st.columns(2)
                    with col1:
                        update_button = st.form_submit_button("Update Portfolio")
                    with col2:
                        delete_button = st.form_submit_button("Delete Portfolio")

                    if update_button:
                        if edited_title and edited_description and edited_tech_stack:
                            cursor.execute("UPDATE Portfolios SET project_title = ?, project_description = ?, project_tech_stack = ? WHERE portfolio_id = ?",
                                           (edited_title, edited_description, edited_tech_stack, portfolio[0]))
                            conn.commit()
                            st.success("Portfolio updated successfully!")
                            st.rerun()
                        else:
                            st.error("Please fill in all fields.")
                    
                    if delete_button:
                        cursor.execute("DELETE FROM Portfolios WHERE portfolio_id = ?", (portfolio[0],))
                        conn.commit()
                        st.success("Portfolio deleted successfully!")
                        st.rerun()
    else:
        st.info("You don't have any portfolios yet.")

    # Add New Portfolio button
    if st.button("Add New +"):
        st.session_state.show_new_portfolio_form = True

    # Show New Portfolio form
    if st.session_state.get('show_new_portfolio_form', False):
        with st.form(key='add_portfolio_form'):
            st.subheader("Create New Portfolio")
            project_title = st.text_input("Project Title")
            project_description = st.text_area("Project Description")
            project_tech_stack = st.text_input("Technologies (comma-separated)")
            submit_button = st.form_submit_button("Save Portfolio")

            if submit_button:
                if project_title and project_description and project_tech_stack:
                    cursor.execute("INSERT INTO Portfolios (user_id, project_title, project_description, project_tech_stack) VALUES (?, ?, ?, ?)",
                                   (st.session_state.user_id, project_title, project_description, project_tech_stack))
                    conn.commit()
                    st.success("Portfolio created successfully!")
                    st.session_state.show_new_portfolio_form = False
                    st.rerun()
                else:
                    st.error("Please fill in all fields.")

    conn.close()

# Initialize session state
if 'show_new_portfolio_form' not in st.session_state:
    st.session_state.show_new_portfolio_form = False


    