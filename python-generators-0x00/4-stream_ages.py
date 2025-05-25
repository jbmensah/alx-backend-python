#!/usr/bin/python3
"""
Memory-efficient aggregation: compute average age via generator.
"""
from seed import connect_to_prodev

def stream_user_ages():
	"""
	Generator that yields the 'age' of each user one by one.
	"""
	connection = connect_to_prodev()
	cursor = connection.cursor(dictionary=True)
	cursor.execute("SELECT age FROM user_data")
	for row in cursor:
		yield row['age']
	cursor.close()
	connection.close()

def calculate_average_age():
	"""
	Uses stream_user_ages generator to compute and print the average age.
	"""
	total = 0
	count = 0
	for age in stream_user_ages():  # first loop: iterate ages
		total += age
		count += 1
	average = float(total) / count if count else 0
	print(f"Average age of users: {average}")  # second loop implicitly via generator consumption

if __name__ == '__main__':
	calculate_average_age()
