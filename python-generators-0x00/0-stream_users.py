import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

def stream_users():
    """
    Generator function that yields rows from user_data table one by one.
    Uses only one loop and yield.
    """
    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data;")

    for row in cursor:  # one loop
        yield row

    cursor.close()
    connection.close()


if __name__ == "__main__":
    for user in stream_users():
        print(user)
