#!/usr/bin/python3

import os
import csv
import mysql.connector
import uuid


def connect_db():
	"""
	Connect to the MySQL database using environment variables.
	"""
	return mysql.connector.connect(
		host=os.getenv('DB_HOST', 'localhost'),
		user=os.getenv('DB_USER', 'root'),
		password=os.getenv('DB_PASSWORD', ''),
	)

def create_database(connection):
	"""
	Create the ALX_prodev database if it does not exist.
	"""
	cursor = connection.cursor()
	cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
	cursor.execute("USE ALX_prodev;")
	connection.commit()
	cursor.close()

def connect_to_prodev():
	"""
	Connect to the ALX_prodev database.
	"""
	return mysql.connector.connect(
		host=os.getenv('DB_HOST', 'localhost'),
		user=os.getenv('DB_USER', 'root'),
		password=os.getenv('DB_PASSWORD', ''),
		database='ALX_prodev'
	)

def create_table(connection):
	"""
	Create the user_data table if it does not exist.
	"""
	cursor = connection.cursor()
	cursor.execute(
		"""
		CREATE TABLE IF NOT EXISTS user_data (
			user_id VARCHAR(36) PRIMARY KEY,
			name VARCHAR(255) NOT NULL,
			email VARCHAR(255) NOT NULL,
			age DECIMAL NOT NULL
		);
		"""
	)
	connection.commit()
	cursor.close()

def insert_data(connection, data_file):
	"""
	Read rows from the give CSV file and insert them into the user_data table.
	Auto-generate user_id if none is present in the CSV.
	"""
	cursor = connection.cursor()
	with open(data_file, newline='', encoding='utf-8-sig') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			# Create a new UUID if the CSV row does not have a user_id
			if 'user_id' not in row:
				uid = row.get('user_id') or str(uuid.uuid4())
			cursor.execute(
				"""
				INSERT IGNORE INTO user_data (user_id, name, email, age)
				VALUES (%s, %s, %s, %s)
				ON DUPLICATE KEY UPDATE
					name = VALUES(name),
					email = VALUES(email),
					age = VALUES(age);
				""",
				(uid, row['name'], row['email'], row['age'])
			)
	connection.commit()
	cursor.close()

def stream_data(connection):
	"""
	Stream data from the user_data table and print it.
	"""
	cursor = connection.cursor(dictionary=True)
	cursor.execute("SELECT * FROM user_data;")
	for record in cursor:
		yield record
	cursor.close()

	