#!/usr/bin/env python3
"""
Setup script to create a test database with sample data
"""
import sqlite3

def setup_database():
    """Create and populate the example database"""
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            email TEXT
        )
    ''')
    
    # Insert sample data
    sample_users = [
        (1, 'Alice', 25, 'alice@example.com'),
        (2, 'Bob', 35, 'bob@example.com'),
        (3, 'Charlie', 45, 'charlie@example.com'),
        (4, 'Diana', 30, 'diana@example.com'),
        (5, 'Eve', 50, 'eve@example.com'),
        (6, 'Frank', 22, 'frank@example.com'),
        (7, 'Grace', 28, 'grace@example.com'),
        (8, 'Henry', 42, 'henry@example.com'),
    ]
    
    cursor.executemany('INSERT OR REPLACE INTO users (id, name, age, email) VALUES (?, ?, ?, ?)', sample_users)
    
    conn.commit()
    conn.close()
    print("Database setup complete!")

if __name__ == "__main__":
    setup_database()