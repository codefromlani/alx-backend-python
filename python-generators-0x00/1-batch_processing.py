import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

def stream_users_in_batches(batch_size):
    """
    Generator that yields batches of users from user_data table.
    Each batch is a list of dictionaries.
    """
    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data;")

    batch = []
    for row in cursor:  # Loop 1
        batch.append(row)
        if len(batch) == batch_size:
            yield batch
            batch = []

    # Yield any remaining rows
    if batch:
        yield batch

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """
    Processes batches from stream_users_in_batches.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:  # Loop over users
            if user['age'] > 25:
                yield user


if __name__ == "__main__":
    # Example usage: batch_size = 3
    for filtered in batch_processing(3):
        print(filtered)
