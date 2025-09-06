import mysql.connector
import csv
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

def connect_db():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_database(connection):
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};")
        print(f"Database {DB_NAME} ensured")
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")
    finally:
        cursor.close()

def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_table(connection):
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL NOT NULL,
        INDEX (user_id)
    );
    """
    try:
        cursor.execute(create_table_query)
        connection.commit()
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")
    finally:
        cursor.close()

def insert_data(connection, data):
    cursor = connection.cursor()
    try:
        with open(data, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Skip if email already exists
                cursor.execute("SELECT * FROM user_data WHERE email = %s;", (row["email"],))
                if cursor.fetchone():
                    continue

                user_id = str(uuid.uuid4())
                cursor.execute(
                    "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s);",
                    (user_id, row["name"], row["email"], row["age"])
                )
        connection.commit()
        print("Data inserted successfully")
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
    finally:
        cursor.close()

if __name__ == "__main__":
    conn = connect_db()
    if conn:
        create_database(conn)
        conn.close()

    conn = connect_to_prodev()
    if conn:
        create_table(conn)
        insert_data(conn, "user_data.csv")
        conn.close()
