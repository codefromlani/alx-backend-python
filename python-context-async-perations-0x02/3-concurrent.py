import asyncio
import aiosqlite

async def async_fetch_users(db_path="users.db"):
    async with aiosqlite.connect(db_path) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            return rows

async def async_fetch_older_users(db_path="users.db"):
    async with aiosqlite.connect(db_path) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            rows = await cursor.fetchall()
            return rows

async def fetch_concurrently():
    users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    print("All users:", users)
    print("Users older than 40:", older_users)


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
