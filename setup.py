import sqlite3

def setup_database():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    # Create Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT UNIQUE NOT NULL,
        user_password TEXT NOT NULL
    )
    ''')

    # Create Profiles table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Profiles (
        profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        profile_title TEXT,
        profile_description TEXT,
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
    )
    ''')

    # Create Portfolios table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Portfolios (
        portfolio_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        project_title TEXT,
        project_description TEXT,
        project_tech_stack TEXT,
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
    )
    ''')

    # Create Proposal table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Proposals (
        proposal_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        job_title TEXT,
        job_description TEXT,
        chosen_projects TEXT,
        generated_proposal TEXT,
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
    )
    ''')

    # Create Secrets table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Secrets (
        secret_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        secret_name TEXT NOT NULL,
        secret_value TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
    )
    ''')

    conn.commit()
    conn.close()

    print("Database setup completed successfully.")

if __name__ == "__main__":
    setup_database()



    