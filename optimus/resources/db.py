from sqlalchemy import create_engine, text, MetaData, Table, inspect
from sqlalchemy.orm import sessionmaker
from .common import get_db_object_to_dict, get_db_object_to_list, get_db_object_to_list_for_db
import datetime


class Db:
    def __init__(self, db_url):
        self.db_url = db_url

    def create_db_connection(self):
        """
        it is used to create a db connection
        :return: db connection object
        """
        try:
            engine = create_engine(self.db_url)
            connection = engine.connect()
            return connection
        except ConnectionError as e:
            return False

    def check_table_exists(self, connection, table_name):
        """
        it will check whether provided table exists in the database
        :param connection: database connection bject
        :param table_name: table name
        :return: if the table exists it will return True else it will return False
        """
        if connection:
            query = "SHOW TABLES"
            result = self.execute_query(connection, query)
            if result:
                if table_name in get_db_object_to_list_for_db(result):
                    return True
                else:
                    return False
            else:
                return f"Failed to collect table information {table_name}"
        else:
            return "Failed to connect database"

    def check_column_exists(self, connection, table_name, column_list):
        """
        it will check the provided the column exists for the table
        :param connection: database connection object
        :param table_name: table name
        :param column_list: name of the columns
        :return: return True if the table exists
        """
        if connection:
            table_exists_status = self.check_table_exists(connection, table_name)
            if table_exists_status:
                inspector = inspect(connection)

                # Get the list of column names for the specified table
                columns = inspector.get_columns(table_name)
                table_column_list = [item['name'] for item in columns]

                for column in column_list:
                    if column not in table_column_list:
                        return f"column {column} not exists in {table_name}"
                return True
            else:
                return f"Table {table_name} not exists"
        else:
            return "Failed to connect database"

    def execute_query(self, connection, query):
        '''
        the function is used to execute the sql queires
        :param connection: database connection object
        :param query: query string
        :return: it will return the query result
        '''
        if connection and query:
            try:
                result = connection.execute(text(query))
                return result
            except:
                return False

    def get_table_data(self, db_engine, table_name):
        '''
        fucntion used to get the all the data from the table
        :param db_engine: database connection object
        :param table_name: table name
        :return: return dictionary which table name
        '''
        if db_engine:
            table_exists_status = self.check_table_exists(db_engine, table_name)
            if table_exists_status:
                metadata = MetaData()
                table = Table(table_name, metadata, autoload_with=db_engine)
                Session = sessionmaker(bind=db_engine)
                session = Session()
                rows = session.query(table).all()
                if rows:
                    data = [{column.name: getattr(row, column.name) for column in table.columns} for row in rows]
                    return data
                else:
                    return f"Table {table_name} is empty"
            else:
                return f"Table {table_name} not exists"
        else:
            return "Failed to connect to the database"

    def get_column_data_from_table(self, db_engine, table_name, columns_to_retrieve):
        '''
            fucntion used to get the columns mentioned in the parameter
            :param db_engine: database connection object
            :param table_name: table name
            :return: return dictionary which table name
        '''
        if db_engine:
            table_exists_status = self.check_table_exists(db_engine, table_name)
            if table_exists_status:
                metadata = MetaData()
                table = Table(table_name, metadata, autoload_with=db_engine)
                Session = sessionmaker(bind=db_engine)
                session = Session()
                # Fetch specified columns from the table
                rows = session.query(*[getattr(table.columns, column) for column in columns_to_retrieve]).all()
                if rows:
                    result = [{column: getattr(row, column) for column in columns_to_retrieve} for row in rows]
                    return result
                else:
                    return f"Table {table_name} is empty"
            else:
                return f"Table {table_name} not exists"
        else:
            return "Failed to connect to the database"
