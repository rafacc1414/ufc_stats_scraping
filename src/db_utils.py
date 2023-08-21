import psycopg2
from tabulate import tabulate


class PostgreSQLDatabase:
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None
        self.connected = False

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                dbname=self.database,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
            )
            self.cursor = self.connection.cursor()
            self.connected = True
            print(f'--- Connected to "{self.database}" database ---')
        except psycopg2.Error as e:
            print(f"Error connecting to the database: {e}")
            self.connected = False

    def disconnect(self):
        if not self.connected:
            print("Not connected to the database.")
            return

        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
                print(f'--- Disconnected from "{self.database}" database ---')
        except psycopg2.Error as e:
            print(f"Error disconnecting from the database: {e}")

    def table_exists(self, tablename):
        if not self.connected:
            print("Not connected to the database.")
            return False

        try:
            query = f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = %s)"
            self.cursor.execute(query, (tablename,))
            return self.cursor.fetchone()[0]

        except psycopg2.Error as e:
            print(f"Error checking table existence: {e}")
            return False

    def row_exists(self, tablename, column_name, column_value):
        if not self.connected:
            print("Not connected to the database.")
            return False

        try:
            query = f'SELECT EXISTS (SELECT 1 FROM "{tablename}" WHERE "{column_name}" = %s)'
            self.cursor.execute(query, (column_value,))
            return self.cursor.fetchone()[0]

        except psycopg2.Error as e:
            print(f"Error checking row existence: {e}")
            return False

    def create_table(self, tablename, columns):
        if not self.connected:
            print("Not connected to the database.")
            return False

        if self.table_exists(tablename):
            print(f'Table "{tablename}" already exists.')
            return False

        try:
            placeholders = ", ".join(["%s"] * len(columns))
            column_definitions = ", ".join(columns)
            query = f'CREATE TABLE "{tablename}" ({column_definitions})'

            self.cursor.execute(query)
            self.connection.commit()
            print(f'--- Table "{tablename}" created successfully ---')
            return True
        except psycopg2.Error as e:
            print(f"Error creating table: {e}")
            return False

    def insert_data(self, tablename, values):
        if not self.connected:
            print("Not connected to the database.")
            return False

        try:
            placeholders = ", ".join(["%s"] * len(values))
            query = f"INSERT INTO {tablename} VALUES ({placeholders})"
            self.cursor.execute(query, values)
            self.connection.commit()
            print("--- Data inserted successfully ---")
            return True
        except psycopg2.Error as e:
            print(f"Error inserting data: {e}")
            return False

    def update_data(self, tablename, name_column, name_value, new_values, column_names):
        if not self.connected:
            print("Not connected to the database.")
            return False

        try:
            if self.row_exists(tablename, name_column, name_value):
                set_columns = ", ".join([f"{col} = %s" for col in column_names])
                set_values = new_values + [name_value]
                query = f"UPDATE {tablename} SET {set_columns} WHERE {name_column} = %s"
                self.cursor.execute(query, set_values)
                self.connection.commit()
                print(f"--- Row updated successfully ---")
                return True
            else:
                print(f'Row with {name_column} "{name_value}" does not exist.')
                return False

        except psycopg2.Error as e:
            print(f"Error updating row: {e}")
            return False

    def get_table_data(self, tablename):
        if not self.connected:
            print("Not connected to the database.")
            return None

        try:
            query = f"SELECT * FROM {tablename}"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            column_names = [desc[0] for desc in self.cursor.description]
            table_data = []
            for row in rows:
                row_dict = dict(zip(column_names, row))
                table_data.append(row_dict)
            return table_data

        except psycopg2.Error as e:
            print(f"Error fetching data: {e}")
            return None

    def drop_column(self, tablename, column_name):
        if not self.connected:
            print("Not connected to the database.")
            return False

        try:
            query = f"ALTER TABLE {tablename} DROP COLUMN {column_name}"
            self.cursor.execute(query)
            self.connection.commit()
            print(f'--- Column "{column_name}" dropped from table "{tablename}"')
            return True
        except psycopg2.Error as e:
            print(f"Error dropping column: {e}")
            return False

    def drop_table(self, tablename):
        if not self.connected:
            print("Not connected to the database.")
            return False

        try:
            query = f"DROP TABLE IF EXISTS {tablename}"
            self.cursor.execute(query)
            self.connection.commit()
            print("--- Table deleted successfully ---")
            return True
        except psycopg2.Error as e:
            print(f"Error deleting table: {e}")
            return False

    def execute_query(self, query):
        if not self.connected:
            print("Not connected to the database.")
            return False

        try:
            self.cursor.execute(query)
            self.connection.commit()
            rows = self.cursor.fetchall()
            column_names = [desc[0] for desc in self.cursor.description]
            print(tabulate(rows, headers=column_names, tablefmt="psql"))
            print("--- Query executed successfully ---")
            return True
        except psycopg2.Error as e:
            print(f"Error executing query: {e}")
            return False
