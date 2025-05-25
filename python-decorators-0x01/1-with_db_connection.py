import sqlite3
import functools

def with_db_connection(func):
	"""
	Opens a SQLite connection (users.db), passes it as the first argument
	to `func`, then closes it when done (even on error).
	"""
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		conn = sqlite3.connect('users.db')
		try:
			# Call the wrapped function, inserting conn at the front
			return func(conn, *args, **kwargs)
		finally:
			conn.close()
	return wrapper

@with_db_connection 
def get_user_by_id(conn, user_id):
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
	return cursor.fetchone()

#### Fetch user by ID with automatic connection handling 
user = get_user_by_id(user_id=1)
print(user)
