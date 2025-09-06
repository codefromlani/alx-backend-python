from seed import connect_db

def paginate_users(page_size: int, offset: int):
    """
    Fetch a single page of users from the database starting at offset.
    Returns a list of user dictionaries.
    """
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("USE ALX_prodev")

    cursor.execute(
        f"SELECT user_id, name, email, age FROM user_data LIMIT {page_size} OFFSET {offset}"
    )
    rows = cursor.fetchall()

    # Build list of dictionaries
    users = [{"user_id": row[0], "name": row[1], "email": row[2], "age": int(row[3])} for row in rows]

    cursor.close()
    return users


def lazy_paginate(page_size: int):
    """
    Generator that yields pages of users lazily, using paginate_users.
    """
    offset = 0

    while True:  # Only one loop
        page = paginate_users(page_size, offset)
        if not page:
            break  # No more pages
        yield page
        offset += page_size


if __name__ == "__main__":
    for page in lazy_paginate(3):
        print(page)
