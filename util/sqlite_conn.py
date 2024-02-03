import sqlite3

from util.logger import setup_logger


class SQLiteConnection:
    """
    A class for managing SQLite database connections.

    Attributes:
    - db_name (str): The name of the SQLite database file.
    - conn (sqlite3.Connection): The SQLite database connection object.

    Methods:
    - __init__(self, db_name: str): Constructor to initialize the SQLite connection.
    - connect(self): To create a sqlite database
    - create_table(self, create_table_query: str) -> None:
        To create table using a sql create statement
    - insert_data(self, table_name: str, data) -> None: To insert the records into the sqlite table
    - insert_dataframe(self, table_name: str, df, insert_type='append') -> None:
        To insert the records of a dataframe into the sqlite table
    - execute_query(self, sql_query: str):
        Executes a SQL script containing sql query and return the result of it.
    - close_connection(self) -> None: Closes the SQLite database connection.
    """

    def __init__(self, db_name: str):
        """
        Constructor to initialize the SQLite connection.
        - param db_name (str): The name of the SQLite database file.
        """
        self.db_name = db_name
        self.conn = None
        self.logger = setup_logger()

    # create a sqlite database
    def connect(self) -> None:
        """
        Method to create a sqlite database
        """
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.logger.info(f"Connected to database: {self.db_name}")
        except sqlite3.Error as e:
            self.logger.debug(f"Error connecting to database: {e}")

    def create_table(self, create_table_query: str) -> None:
        """
        Method to create table using a sql create statement
        - param create_table_query: Create statement sql query
        """
        try:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute(create_table_query)
                # self.logger.info(f"Table created successfully")
        except sqlite3.Error as e:
            self.logger.debug(f"Error creating table: {e}")

    def insert_data(self, table_name: str, data) -> None:
        """
        Method to insert the records into the sqlite table
        - param table_name: Name of the table in which data is to be inserted
        - param data: Data that needs to be inserted
        """
        try:
            with self.conn:
                cursor = self.conn.cursor()
                columns = ", ".join(data.keys())
                values = ", ".join(["?" for _ in range(len(data))])
                insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
                cursor.execute(insert_query, tuple(data.values()))
                # self.logger.info(f"Data inserted into table {table_name} successfully")
        except sqlite3.Error as e:
            self.logger.debug(f"Error inserting data into table {table_name}: {e}")

    def insert_dataframe(self, table_name: str, df, insert_type="append") -> None:
        """
        Method to insert the records of a dataframe into the sqlite table
        - param table_name: Name of the table in which data is to be inserted
        - param df: Dataframe whose data needs to be inserted
        - param insert_type: behavior if the table already exists. ['fail', 'replace', 'append']
        """
        try:
            with self.conn:
                df.to_sql(table_name, self.conn, if_exists=insert_type, index=False)
                # self.logger.info(f"DF inserted into table {table_name} successfully")
        except sqlite3.Error as e:
            self.logger.debug(f"Error inserting data into table {table_name}: {e}")

    def execute_query(self, sql_query: str):
        """
        Executes a SQL script containing sql query and return the result of it.
        - param sql_query (str): The SQL script to be executed.
        """
        try:
            with self.conn:
                cursor = self.conn.cursor()
                cursor.execute(sql_query)
                results = cursor.fetchall()
                # self.logger.info("Query executed successfully.")
                return results
        except sqlite3.Error as e:
            self.logger.debug(f"Error executing sql: {e}")
            return None

    def close_connection(self) -> None:
        """
        Closes the SQLite database connection.
        """
        if self.conn:
            self.conn.close()
            self.logger.info("Connection closed")
        else:
            self.info("No active connection to close")
