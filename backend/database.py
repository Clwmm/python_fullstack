import sqlite3

# SQLite database file
DB_FILE = "./test.db"

# Function to get a connection to the SQLite database
def get_db():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    # Optional: To return rows as dictionaries
    conn.row_factory = sqlite3.Row
    return conn

# Initialize the database by creating tables
def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Create a 'users' table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    ''')
    
    conn.commit()
    conn.close()
