import sqlite3
import functools

def with_db_connection(func):
	"""
	Opens 'users.db', passes the connection as the first arg to func,
	then closes it when done (even on error).
	"""
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		conn = sqlite3.connect('users.db')
		try:
			return func(conn, *args, **kwargs)
		finally:
			conn.close()
	return wrapper

def transactional(func):
	"""
	Wraps a DB operation in a transaction:
	• commit() if func succeeds
	• rollback() if func raises an exception
	"""
	@functools.wraps(func)
	def wrapper(conn, *args, **kwargs):
		try:
			result = func(conn, *args, **kwargs)
			conn.commit()
			print("[LOG] Transaction committed")
			return result
		except Exception as e:
			conn.rollback()
			print(f"[LOG] Transaction rolled back due to: {e}")
			raise
	return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
	cursor = conn.cursor()
	cursor.execute(
		"UPDATE users SET email = ? WHERE id = ?",
		(new_email, user_id)
	)
	# no commit here — handled by @transactional

if __name__ == '__main__':
	# Example run: update user #1’s email
	update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
