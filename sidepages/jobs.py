import streamlit as st
import sqlite3
from .scrapper import scrape_upwork_jobs
from streamlit.runtime.scriptrunner import add_script_run_ctx

def show_scrap_jobs():
    st.header("Scrape Upwork Jobs")
    st.write("Here you can scrape jobs from Upwork based on your search query.")

    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    # Fetch secrets for the current user
    cursor.execute("SELECT secret_id, secret_name, secret_value FROM Secrets WHERE user_id = ?", (st.session_state.user_id,))
    secrets = cursor.fetchall()

    if secrets:
        secret_names = [secret[1] for secret in secrets]
        
        username_secret = st.selectbox("Select Username Secret", secret_names, key="username_secret")
        password_secret = st.selectbox("Select Password Secret", secret_names, key="password_secret")
        
        # Find the selected secrets' values
        username = next((secret[2] for secret in secrets if secret[1] == username_secret), None)
        password = next((secret[2] for secret in secrets if secret[1] == password_secret), None)

        search_query = st.text_input("Enter Search Query")

        if st.button("Refresh Jobs"):
            if username and password and search_query:
                with st.spinner("Scraping jobs..."):
                    try:
                        jobs = scrape_upwork_jobs(username, password, search_query)
                        st.session_state.scraped_jobs = jobs
                        st.success(f"Successfully scraped {len(jobs)} jobs!")
                    except Exception as e:
                        st.error(f"An error occurred while scraping: {str(e)}")
            else:
                st.warning("Please select both username and password secrets, and enter a search query.")

        if 'scraped_jobs' in st.session_state and st.session_state.scraped_jobs:
            st.subheader("Scraped Jobs")
            for index, job in enumerate(st.session_state.scraped_jobs):
                with st.expander(job['title']):
                    st.write(f"Description: {job['description']}")
                    st.write(f"Link: {job['link']}")
                    def on_generate_proposal():
                        st.session_state.selected_job = {
                            'title': job['title'],
                            'description': job['description']
                        }
                        st.session_state.page = "Proposal Generation"

                    if st.button("Generate Proposal", key=f"generate_proposal_{index}", on_click=on_generate_proposal):
                        st.rerun()

    else:
        st.warning("You don't have any secrets stored yet. Add secrets in the Settings page.")

    conn.close()

# Initialize session state
if 'scraped_jobs' not in st.session_state:
    st.session_state.scraped_jobs = []
if 'selected_job' not in st.session_state:
    st.session_state.selected_job = None
if 'proposal_generation_state' not in st.session_state:
    st.session_state.proposal_generation_state = {}


