from dotenv import load_dotenv
import os
import mysql.connector

# 1. Load env vars
load_dotenv()

class DatabaseConnection:
	def __init__(self):
		self.host     = os.getenv("DB_HOST")
		self.user     = os.getenv("DB_USER")
		self.password = os.getenv("DB_PASSWORD")
		self.database = os.getenv("DB_NAME")
		self.port     = int(os.getenv("DB_PORT", 3306))
		self.conn     = None

	def __enter__(self):
		self.conn = mysql.connector.connect(
			host     = self.host,
			user     = self.user,
			password = self.password,
			database = self.database,
			port     = self.port
		)
		return self.conn

	def __exit__(self, exc_type, exc_val, exc_tb):
		if exc_type:
			self.conn.rollback()
		else:
			self.conn.commit()
		self.conn.close()

# 3. Demo: query and print all users
if __name__ == "__main__":
	with DatabaseConnection() as conn:
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM users")
		for row in cursor:
			print(row)
