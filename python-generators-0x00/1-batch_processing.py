#!/usr/bin/python3
"""
Batch processing for user_data table using generators.
"""

from seed import connect_to_prodev

def stream_users_in_batches(batch_size):
	"""
	Generator that yields lists of user records from user_data table in batches.
	"""
	connection = connect_to_prodev()
	# Use buffered cursor to avoid "Unread result found" on close
	cursor = connection.cursor(dictionary=True, buffered=True)
	cursor.execute("SELECT * FROM user_data")
	try:
		while True:
			batch = cursor.fetchmany(batch_size)
			if not batch:
				break
			yield batch
	finally:
		cursor.close()
		connection.close()


def batch_processing(batch_size):
	"""
	Processes batches of users and prints users whose age > 25.
	"""
	for batch in stream_users_in_batches(batch_size):
		for user in batch:
			# age is Decimal, compare > 25
			if user.get('age', 0) > 25:
				print(user)
