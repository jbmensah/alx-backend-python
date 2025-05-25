#!/usr/bin/python3
"""
Batch processing for user_data table.
"""
from seed import connect_to_prodev

def stream_users_in_batches(batch_size):
	"""
	Connects to ALX_prodev and yields rows from user_data in batches.
	"""
	connection = connect_to_prodev()
	cursor = connection.cursor(dictionary=True)
	cursor.execute("SELECT * FROM user_data;")
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
			if user.get('age', 0) > 25:
				yield user
			print(user)