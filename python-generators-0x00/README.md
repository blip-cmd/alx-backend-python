# 0. Getting started with python generators

This script sets up a MySQL database `ALX_prodev` and a table `user_data` with the following fields:
- user_id (Primary Key, UUID, Indexed)
- name (VARCHAR, NOT NULL)
- email (VARCHAR, NOT NULL)
- age (DECIMAL, NOT NULL)

It also populates the table with data from `user_data.csv`.

## Usage

1. Ensure you have MySQL running and the `mysql-connector-python` package installed:
   ```sh
   pip install mysql-connector-python
   ```
2. Place your `user_data.csv` in the same directory as `seed.py`.
3. Run the main script (see `0-main.py` for example usage).

## Functions
- `connect_db()`: Connects to the MySQL server.
- `create_database(connection)`: Creates the `ALX_prodev` database if it does not exist.
- `connect_to_prodev()`: Connects to the `ALX_prodev` database.
- `create_table(connection)`: Creates the `user_data` table if it does not exist.
- `insert_data(connection, data)`: Inserts data from the CSV file into the table if not already present.

## Example
See `0-main.py` for a sample workflow.
