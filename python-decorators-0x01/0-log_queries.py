import functools
import sqlite3
from datetime import datetime

def log_queries(func):
	"""
	Decorator that logs the SQL query before executing the wrapped function.
	Assumes the SQL is passed in as either:
	- a keyword argument named 'query', or
	- the first positional argument.
	"""
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		# 1. Extract the SQL string
		if 'query' in kwargs:
			sql = kwargs['query']
		elif args:
			sql = args[0]
		else:
			sql = None

		# 2. Log it
		print(f"[LOG] Executing SQL Query: {sql}")

		# 3. Call the original function
		return func(*args, **kwargs)

	return wrapper

@log_queries
def fetch_all_users(query):
    conn    = sqlite3.connect('users.db')
    cursor  = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# …later in your code…
users = fetch_all_users(query="SELECT * FROM users")