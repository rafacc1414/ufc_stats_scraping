import psycopg2
#from tabulate import tabulate

class PostgreSQLDatabase:
    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password,
        )
        self.cursor = self.connection.cursor()
        print(f'--- Connected to "{self.database}" database ---')

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print(f'--- Disconnected from "{self.database}" database ---')

    def execute_query(self, query):
        self.cursor.execute(query)
        self.connection.commit()
        rows = self.cursor.fetchall()
        # WIP : Trying to show the result of the query using 'tabulate'
        #column_names = [desc[0] for desc in self.cursor.description]
        #print(tabulate(rows, headers=column_names, tablefmt='psql'))
        print("--- Query executed succesfully ---")

    def drop_table(self, tablename):
        query = f"DROP TABLE IF EXISTS {tablename}"
        self.cursor.execute(query)
        self.connection.commit()
        print("--- Table deleted succesfully ---")
