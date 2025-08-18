import mysql.connector

def stream_user_ages():
    """Generator that yields user ages one by one from user_data table."""
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # Set your MySQL root password if needed
            database='ALX_prodev'
        )
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data;")
        for (age,) in cursor:
            yield age
    except Exception as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def average_user_age():
    """Calculates and prints the average age of users using a generator."""
    total = 0
    count = 0
    for age in stream_user_ages():
        total += float(age)
        count += 1
    avg = total / count if count else 0
    print(f"Average age of users: {avg}")
