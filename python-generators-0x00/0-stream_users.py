import mysql.connector

def stream_users():
    """Generator that yields rows from user_data table one by one as dicts."""
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # Set your MySQL root password if needed
            database='ALX_prodev'
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")
        for row in cursor:
            yield row
    except Exception as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
