from sqlite3 import Connection

# Function to create a new user in the database
def create_user(conn: Connection, name: str, email: str, password: str):
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
        INSERT INTO users (name, email, password) 
        VALUES (?, ?, ?)
        ''', (name, email, password))
        conn.commit()
        return cursor.lastrowid  # Return the ID of the inserted user
    except sqlite3.IntegrityError:
        raise ValueError("Email already registered")
    finally:
        cursor.close()  # Ensure the cursor is closed after the operation

# Function to get a user by email
def get_user_by_email(conn: Connection, email: str):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    cursor.close()  # Close the cursor
    return user

# Function to get all users
def get_users(conn: Connection):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    cursor.close()  # Close the cursor
    return users
