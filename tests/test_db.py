import os
import unittest
import psycopg2

# TODO: Use environment variables to store this information
# POSTGRES_DB = os.environ.get('POSTGRES_DB')
# POSTGRES_USER = os.environ.get('POSTGRES_USER')
# POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')

# Database information
POSTGRES_DB = "postgres"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "postgres"
POSTGRES_HOST="localhost"
POSTGRES_PORT="5432"

class TestPostgreSQL(unittest.TestCase):
    def setUp(self):
        # Establish a connection to the PostgreSQL database
        self.conn = psycopg2.connect(
            dbname=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT
        )

        # Create a cursor object to execute SQL queries
        self.cur = self.conn.cursor()

        # Check if the test table already exists
        self.cur.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'test_table')")
        table_exists = self.cur.fetchone()[0]

        if not table_exists:
            # Create the test table
            self.cur.execute("CREATE TABLE test_table (id SERIAL PRIMARY KEY, name VARCHAR)")

        # Commit the changes to the database
        self.conn.commit()

    def tearDown(self):
        # Drop the test table
        self.cur.execute("DROP TABLE IF EXISTS test_table")

        # Commit the changes to the database
        self.conn.commit()

        # Close the cursor and connection
        self.cur.close()
        self.conn.close()

    def test_insert_data(self):
        # Insert test data into the table
        self.cur.execute("INSERT INTO test_table (name) VALUES ('John')")
        self.conn.commit()

        # Query the table to verify the inserted data
        self.cur.execute("SELECT * FROM test_table WHERE name = 'John'")
        result = self.cur.fetchone()

        # Assert that the query result matches the inserted data
        self.assertEqual(result[1], 'John')

    def test_update_data(self):
        # Insert initial data into the table
        self.cur.execute("INSERT INTO test_table (name) VALUES ('Jane')")
        self.conn.commit()

        # Update the inserted data
        self.cur.execute("UPDATE test_table SET name = 'Janet' WHERE name = 'Jane'")
        self.conn.commit()

        # Query the table to verify the updated data
        self.cur.execute("SELECT * FROM test_table WHERE name = 'Janet'")
        result = self.cur.fetchone()

        # Assert that the query result matches the updated data
        self.assertEqual(result[1], 'Janet')

    def test_show_tables(self):
        # Query the PostgreSQL database for a list of all tables
        self.cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")

        # Fetch all the table names
        table_names = self.cur.fetchall()

        # Print the table names
        for table_name in table_names:
            print(table_name[0])

    # Add more test cases as needed

if __name__ == '__main__':
    unittest.main()




