#!/usr/bin/python3
"""
Generator for streaming rows from user_data table one by one.
"""
from seed import connect_to_prodev

def stream_users():
	"""
	Connects to ALX_prodev and yields each row from user_data as a dict.
	"""
	connection = connect_to_prodev()
	cursor = connection.cursor(dictionary=True)
	cursor.execute("SELECT * FROM user_data;")
	for record in cursor:
		yield record
	cursor.close()
	connection.close()