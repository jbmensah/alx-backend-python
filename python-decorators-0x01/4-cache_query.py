import time
import sqlite3
import functools

# —————————————————————————————
# Global cache store
# —————————————————————————————
query_cache = {}

# —————————————————————————————
# 1) Connection decorator
# —————————————————————————————
def with_db_connection(func):
	"""
	Opens 'users.db', passes the conn as first arg to func,
	then always closes it afterward.
	"""
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		conn = sqlite3.connect('users.db')
		try:
			return func(conn, *args, **kwargs)
		finally:
			conn.close()
	return wrapper

# —————————————————————————————
# 2) Caching decorator
# —————————————————————————————
def cache_query(func):
	"""
	Caches the result of a query (keyed by the SQL string) so that
	repeated calls with the same query return the cached result instantly.
	"""
	@functools.wraps(func)
	def wrapper(conn, *args, **kwargs):
		# 1) Extract the SQL query string
		if 'query' in kwargs:
			sql = kwargs['query']
		elif args:
			sql = args[0]
		else:
			raise ValueError("cache_query: no SQL query provided")

		# 2) Return cached if present
		if sql in query_cache:
			print(f"[CACHE] Returning cached result for query: {sql}")
			return query_cache[sql]

		# 3) Otherwise, execute and cache
		result = func(conn, *args, **kwargs)
		query_cache[sql] = result
		print(f"[CACHE] Caching result for query: {sql}")
		return result

	return wrapper

# —————————————————————————————
# 3) Decorated function
# —————————————————————————————
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
	cursor = conn.cursor()
	cursor.execute(query)
	return cursor.fetchall()

# —————————————————————————————
# 4) Demo
# —————————————————————————————
if __name__ == '__main__':
	# First call: not in cache yet
	users = fetch_users_with_cache(query="SELECT * FROM users")
	print("First fetch:", users)

	# Second call: should hit cache
	users_again = fetch_users_with_cache(query="SELECT * FROM users")
	print("Second fetch:", users_again)
