import asyncio
import aiosqlite

DB_PATH = "users.db"  # Path to your SQLite database file

async def async_fetch_users():
	"""
	Fetch all users from the users table.
	"""
	async with aiosqlite.connect(DB_PATH) as db:
		db.row_factory = aiosqlite.Row
		async with db.execute("SELECT * FROM users") as cursor:
			return await cursor.fetchall()

async def async_fetch_older_users():
	"""
	Fetch users older than 40.
	"""
	async with aiosqlite.connect(DB_PATH) as db:
		db.row_factory = aiosqlite.Row
		async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
			return await cursor.fetchall()

async def fetch_concurrently():
	"""
	Run both fetch queries concurrently and print results.
	"""
	users, older_users = await asyncio.gather(
		async_fetch_users(),
		async_fetch_older_users()
	)

	print("All users:")
	for user in users:
		print(dict(user))

	print("\nUsers older than 40:")
	for user in older_users:
		print(dict(user))

if __name__ == "__main__":
	asyncio.run(fetch_concurrently())
# This script demonstrates how to fetch data from a SQLite database concurrently using asyncio and aiosqlite.