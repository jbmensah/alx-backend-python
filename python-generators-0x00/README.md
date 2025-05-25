# Task 0: Getting Started with Python Generators

**Objective:**
Create a generator that streams rows from an SQL database one by one.

## Files

- `seed.py`: Script to set up and populate the MySQL database, and provide a streaming generator.
- `0-main.py`: Test harness that uses the functions in `seed.py`.

## Requirements

- Python 3.x
- MySQL server running locally or remotely
- Python package: `mysql-connector-python`

## Setup & Usage

1. **Install dependencies**:
   ```bash
   pip install mysql-connector-python
   ```

2. **Configure environment variables** (optional; defaults shown):
   ```bash
   export MYSQL_HOST=localhost
   export MYSQL_PORT=3306
   export MYSQL_USER=root
   export MYSQL_PASSWORD=""
   ```

3. **Seed the database**:
   ```bash
   chmod +x 0-main.py
   ./0-main.py
   ```

   You should see output similar to:
   ```text
   connection successful
   Table user_data created successfully
   Database ALX_prodev is present
   [('00234e50-34eb-4ce2-94ec-26e3fa749796', ...), ...]
   ```

## seed.py Functions

- `connect_db()` — Connect to the MySQL server (no database).
- `create_database(connection)` — Create the `ALX_prodev` database if missing.
- `connect_to_prodev()` — Connect to the `ALX_prodev` database.
- `create_table(connection)` — Create the `user_data` table.
- `insert_data(connection, data_file)` — Insert rows from CSV, skipping duplicates.
- `stream_data(connection)` — **Generator** that yields rows from `user_data` one at a time.

## Example: Using the Generator

```python
from seed import connect_to_prodev, stream_data

conn = connect_to_prodev()
for row in stream_data(conn):
    print(row)
conn.close()
```

## License

This project is part of the ALX ProDev curriculum.
