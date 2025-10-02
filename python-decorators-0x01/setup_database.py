import sqlite3

# Create a simple users database for testing
def setup_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    
    # Insert sample data
    cursor.execute("DELETE FROM users")  # Clear existing data
    sample_users = [
        (1, 'John Doe', 'john@example.com'),
        (2, 'Jane Smith', 'jane@example.com'),
        (3, 'Bob Johnson', 'bob@example.com')
    ]
    
    cursor.executemany("INSERT INTO users (id, name, email) VALUES (?, ?, ?)", sample_users)
    conn.commit()
    conn.close()
    print("Database setup complete!")

if __name__ == "__main__":
    setup_database()