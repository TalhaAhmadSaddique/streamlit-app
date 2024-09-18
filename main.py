import streamlit as st
from setup import setup_database
from auth.signup import signup
from auth.signin import signin
from sidepages.profiles import show_profiles
from sidepages.portfolios import show_portfolios
from sidepages.settings import show_settings
from sidepages.proposal_generation import show_proposal_generation
from sidepages.jobs import show_scrap_jobs

setup_database()

def show_sidebar():
    with st.sidebar:
        st.write(f"Welcome, User {st.session_state.user_id}!")
        
        # Navigation menu
        def on_page_change():
            st.session_state.page = st.session_state.nav_selection

        st.session_state.page = st.radio(
            "Navigation",
            ["Profiles", "Portfolios", "Jobs", "Proposal Generation", "Settings"],
            index=["Profiles", "Portfolios", "Jobs", "Proposal Generation", "Settings"].index(st.session_state.page),
            key="nav_selection",
            on_change=on_page_change
        )
        
        if st.button("Logout"):
            st.session_state.user_id = None
            st.session_state.page = "Profiles"  # Reset to default page
            st.rerun()

def main():
    # Initialize user_id and page if they don't exist
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'page' not in st.session_state:
        st.session_state.page = "Profiles"  # Set default page

    st.title("Automated Upwork")

    if st.session_state.user_id is not None:
        show_sidebar()
        
        # Display the selected page
        if st.session_state.page == "Profiles":
            show_profiles()
        elif st.session_state.page == "Portfolios":
            show_portfolios()
        elif st.session_state.page == "Proposal Generation":
            show_proposal_generation()
        elif st.session_state.page == "Settings":
            show_settings()
        elif st.session_state.page == "Jobs":
            show_scrap_jobs()
    else:
        # Create two columns for the buttons
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Sign Up", use_container_width=True):
                st.session_state.show_form = "signup"

        with col2:
            if st.button("Sign In", use_container_width=True):
                st.session_state.show_form = "signin"

        # Display the appropriate form based on the button clicked
        if "show_form" in st.session_state:
            if st.session_state.show_form == "signup":
                signup()
            elif st.session_state.show_form == "signin":
                signin()
            
            # Check if user has been authenticated after form submission
            if st.session_state.user_id is not None:
                st.rerun()

if __name__ == "__main__":
    main()


    