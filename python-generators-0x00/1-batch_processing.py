from seed import connect_db

def stream_users_in_batches(batch_size: int):
    """
    Generator that yields batches of users from user_data table.
    Each batch is a list of dictionaries.
    """
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("USE ALX_prodev")

    offset = 0
    while True:
        cursor.execute(f"SELECT user_id, name, email, age FROM user_data LIMIT {batch_size} OFFSET {offset}")
        rows = cursor.fetchall()

        if rows:
            batch = [{"user_id": row[0], "name": row[1], "email": row[2], "age": int(row[3])} for row in rows]
            yield batch
            offset += batch_size
        else:
            break  

    cursor.close()
    return


def batch_processing(batch_size: int):
    """
    Processes batches from stream_users_in_batches.
    Filters users over age 25.
    Yields each user individually.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                yield user



if __name__ == "__main__":
    for user in batch_processing(3):  
        print(user)
