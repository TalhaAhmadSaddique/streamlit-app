import streamlit as st
import sqlite3
import openai

def proposal_generation(profile, portfolios, job_title, job_description, openai_api_key):
    system_prompt = "You are a helpful assistant specialized in generating professional job proposals."
    
    user_prompt = f"""
    Generate a compelling job proposal for the following position:
    Job Title: {job_title}
    Job Description: {job_description}

    Use the following information about the applicant:
    Profile Title: {profile[1]}
    Profile Description: {profile[2]}

    Relevant Portfolio Projects:
    """

    for portfolio in portfolios:
        user_prompt += f"""
    - Project: {portfolio[1]}
      Description: {portfolio[2]}
      Technologies: {portfolio[3]}
        """

    user_prompt += "\nPlease create a well-structured proposal that highlights the applicant's skills and experience in relation to the job requirements."

    try:
        # api_key = openai_api_key
        # client = openai.OpenAI(api_key=api_key)
        # response = client.chat.completions.create(
        #     model="gpt-3.5-turbo",
        #     messages=[
        #         {"role": "system", "content": system_prompt},
        #         {"role": "user", "content": user_prompt}
        #     ]
        # )
        # result = response.choices[0].message.content
        return user_prompt
    except Exception as e:
        return f"An error occurred while generating the proposal: {str(e)}"


def show_proposal_generation():
    st.header("Proposal Generation")
    st.write("Here you can generate proposals for your projects.")

    # Initialize proposal_generation_state if not exists
    if 'proposal_generation_state' not in st.session_state:
        st.session_state.proposal_generation_state = {}

    # Use the selected job from the session state
    if 'selected_job' in st.session_state and st.session_state.selected_job:
        job_title = st.text_input("Job Title", value=st.session_state.selected_job['title'])
        job_description = st.text_area("Job Description", value=st.session_state.selected_job['description'])
        # Store these values in proposal_generation_state
        st.session_state.proposal_generation_state['job_title'] = job_title
        st.session_state.proposal_generation_state['job_description'] = job_description
    else:
        job_title = st.text_input("Job Title", value=st.session_state.proposal_generation_state.get('job_title', ''))
        job_description = st.text_area("Job Description", value=st.session_state.proposal_generation_state.get('job_description', ''))

    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    # Fetch profiles for the current user
    cursor.execute("SELECT profile_id, profile_title, profile_description FROM Profiles WHERE user_id = ?", (st.session_state.user_id,))
    profiles = cursor.fetchall()

    if profiles:
        profile_titles = [profile[1] for profile in profiles]
        
        def on_profile_change():
            st.session_state.proposal_generation_state['selected_profile'] = st.session_state.selected_profile

        selected_profile = st.selectbox("Select a profile", profile_titles, 
                                        index=profile_titles.index(st.session_state.proposal_generation_state.get('selected_profile', profile_titles[0])),
                                        key='selected_profile',
                                        on_change=on_profile_change)
        
        selected_profile_data = next((p for p in profiles if p[1] == selected_profile), None)
    else:
        st.warning("You don't have any profiles yet. Add profiles in the Profiles page.")

    # Fetch portfolios for the current user
    cursor.execute("SELECT portfolio_id, project_title, project_description, project_tech_stack FROM Portfolios WHERE user_id = ?", (st.session_state.user_id,))
    portfolios = cursor.fetchall()

    if portfolios:
        portfolio_titles = [portfolio[1] for portfolio in portfolios]
        
        def on_portfolio_change():
            st.session_state.proposal_generation_state['selected_portfolios'] = st.session_state.selected_portfolios

        selected_portfolios = st.multiselect("Select portfolios (1-3)", portfolio_titles, 
                                             default=st.session_state.proposal_generation_state.get('selected_portfolios', []),
                                             key='selected_portfolios',
                                             on_change=on_portfolio_change)
        
        if len(selected_portfolios) < 1 or len(selected_portfolios) > 3:
            st.warning("Please select 1 to 3 portfolios.")
        
        selected_portfolios_data = [p for p in portfolios if p[1] in selected_portfolios]
    else:
        st.warning("You don't have any portfolios yet. Add portfolios in the Portfolios page.")

    # Function to fetch secrets
    def fetch_secrets():
        cursor.execute("SELECT secret_id, secret_name, secret_value FROM Secrets WHERE user_id = ?", (st.session_state.user_id,))
        return cursor.fetchall()

    # Fetch and display secrets
    secrets = fetch_secrets()
    if secrets:
        secret_names = [secret[1] for secret in secrets]
        
        def on_secret_change():
            st.session_state.proposal_generation_state['selected_secret'] = st.session_state.selected_secret

        selected_secret = st.selectbox("Select OPENAI_API_KEY secret", secret_names,
                                       key='selected_secret',
                                       on_change=on_secret_change)

        # Find the selected secret's value
        selected_secret_value = next((secret[2] for secret in secrets if secret[1] == selected_secret), None)

        if selected_secret_value:
            st.write(f"Secret Value: {selected_secret_value}")
    else:
        st.warning("You don't have any secrets stored yet. Add secrets below or in the Settings page.")

    # New feature: Add new secret key
    if 'show_secret_form' not in st.session_state:
        st.session_state.show_secret_form = False

    if st.button("Add New Secret"):
        st.session_state.show_secret_form = True

    if st.session_state.show_secret_form:
        with st.form(key='add_secret_form'):
            new_secret_name = st.text_input("Secret Name")
            new_secret_value = st.text_input("Secret Value", type="password")
            submit_button = st.form_submit_button(label='Save Secret')

            if submit_button:
                if new_secret_name and new_secret_value:
                    try:
                        cursor.execute("INSERT INTO Secrets (user_id, secret_name, secret_value) VALUES (?, ?, ?)",
                                       (st.session_state.user_id, new_secret_name, new_secret_value))
                        conn.commit()
                        st.success(f"Secret '{new_secret_name}' added successfully!")
                        st.session_state.show_secret_form = False
                        secrets = fetch_secrets()  # Refresh secrets
                        st.rerun()
                    except sqlite3.Error as e:
                        st.error(f"An error occurred: {e}")
                else:
                    st.warning("Please enter both secret name and value.")

    # Generate proposal button
    if st.button("Generate Proposal"):
        if not profiles:
            st.error("Please add at least one profile before generating a proposal.")
        elif not portfolios or len(selected_portfolios) < 1 or len(selected_portfolios) > 3:
            st.error("Please select 1 to 3 portfolios before generating a proposal.")
        elif not secrets:
            st.error("Please add at least one secret before generating a proposal.")
        elif not job_title or not job_description:
            st.error("Please enter both job title and job description.")
        else:
            st.success("Proposal generation started!")
            
            # Generate the proposal
            openai_api_key = selected_secret_value
            generated_proposal = proposal_generation(
                selected_profile_data,
                selected_portfolios_data,
                job_title,
                job_description,
                openai_api_key
            )
            
            # Display the generated proposal
            st.subheader("Generated Proposal")
            st.text_area("Proposal", value=generated_proposal, height=300)

    conn.close()

    # Clear the selected job from session state after using it
    if st.button("Clear Job and Return to Jobs Page"):
        st.session_state.selected_job = None
        st.session_state.proposal_generation_state = {}
        st.session_state.page = "Jobs"
        st.rerun()
        


    