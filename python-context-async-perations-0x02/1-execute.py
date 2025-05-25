from dotenv import load_dotenv
import os
import mysql.connector

# Load environment variables from .env file
load_dotenv()

class ExecuteQuery:
	def __init__(self, query, params=()):
		"""
		Initialize with a raw SQL query and parameters.
		:param query: SQL string, using '?' placeholders for parameters
		:param params: tuple of values to substitute into the query
		"""
		self.raw_query = query
		self.params = params
		self.conn = None
		self.cursor = None
		self.results = None

	def __enter__(self):
		# Establish the database connection
		self.conn = mysql.connector.connect(
			host=os.getenv("DB_HOST"),
			user=os.getenv("DB_USER"),
			password=os.getenv("DB_PASSWORD"),
			database=os.getenv("DB_NAME"),
			port=int(os.getenv("DB_PORT", 3306))
		)
		# Create a cursor for executing queries
		self.cursor = self.conn.cursor()

		# MySQL connector uses '%s' for placeholders, so convert '?' to '%s'
		formatted_query = self.raw_query.replace('?', '%s')
		# Execute the query with the provided parameters
		self.cursor.execute(formatted_query, self.params)
		# Fetch all results
		self.results = self.cursor.fetchall()
		return self.results

	def __exit__(self, exc_type, exc_val, exc_tb):
		# Close the cursor
		if self.cursor:
			self.cursor.close()
		# Commit or rollback based on whether an exception occurred
		if self.conn:
			if exc_type:
				self.conn.rollback()
			else:
				self.conn.commit()
			# Close the connection
			self.conn.close()


if __name__ == "__main__":
	# Example usage: get all users older than 25
	with ExecuteQuery("SELECT * FROM users WHERE age > ?", (25,)) as users:
		for user in users:
			print(user)

	# Example usage: get all users older than 25
	with ExecuteQuery("SELECT * FROM users WHERE age > ?", (25,)) as users:
		for user in users:
			print(user)