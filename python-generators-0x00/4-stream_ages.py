from seed import connect_db

def stream_user_ages():
    """
    Generator that yields user ages one by one.
    """
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("USE ALX_prodev")
    cursor.execute("SELECT age FROM user_data")

    for row in cursor:  # Loop 1
        yield int(row[0])

    cursor.close()
    connection.close()


def calculate_average_age():
    """
    Calculates the average age using the stream_user_ages generator.
    """
    total = 0
    count = 0

    for age in stream_user_ages():  # Loop 2
        total += age
        count += 1

    average = total / count if count > 0 else 0
    return average


if __name__ == "__main__":
    avg_age = calculate_average_age()
    print(f"Average age of users: {avg_age}")
