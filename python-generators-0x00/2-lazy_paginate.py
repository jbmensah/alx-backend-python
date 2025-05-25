#!/usr/bin/python3
"""
Lazy pagination generator for the user_data table.
"""
from seed import connect_to_prodev

def paginate_users(page_size, offset):
	"""
	Fetch a single page of user_data with given page_size and offset.
	Returns a list of row-dicts.
	"""
	connection = connect_to_prodev()
	cursor = connection.cursor(dictionary=True)
	cursor.execute(
		f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}"
	)
	rows = cursor.fetchall()
	cursor.close()
	connection.close()
	return rows


def lazy_pagination(page_size):
	"""
	Generator that lazily yields pages of size `page_size` from user_data.
	Only fetches the next page when needed.
	"""
	offset = 0
	while True:
		page = paginate_users(page_size, offset)
		if not page:
			return  # no more data, end generator
		yield page
		offset += page_size
