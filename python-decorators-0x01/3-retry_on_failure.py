import time
import sqlite3
import functools

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


def retry_on_failure(retries=3, delay=2):
	"""
	If the wrapped function raises, catch and retry up to `retries` times,
	waiting `delay` seconds between attempts. Finally re-raises the last error.
	"""
	def decorator(func):
		@functools.wraps(func)
		def wrapper(conn, *args, **kwargs):
			last_exc = None
			for attempt in range(1, retries + 1):
				try:
					return func(conn, *args, **kwargs)
				except Exception as e:
					last_exc = e
					print(f"[LOG] Attempt {attempt} failed: {e}")
					if attempt < retries:
						print(f"[LOG] Retrying in {delay}s…")
						time.sleep(delay)
			# All attempts exhausted
			print(f"[LOG] All {retries} retries failed. Raising error.")
			raise last_exc
		return wrapper
	return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM users")
	return cursor.fetchall()


if __name__ == '__main__':
	users = fetch_users_with_retry()
	print("Fetched rows:", users)
