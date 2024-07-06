import mysql.connector
from mysql.connector import Error
from urllib.parse import urlparse
from logger import Logger


def create_connection(db_url):
    """
    Create a database connection to the MySQL database.

    Args:
        db_url (str): The database URL.

    Returns:
        mysql.connector.connection.MySQLConnection: The database connection object.
    """
    url = urlparse(db_url)
    user = url.username
    password = url.password
    host = url.hostname
    database = url.path[1:]

    connection = None
    try:
        connection = mysql.connector.connect(
            user=user,
            password=password,
            host=host,
            database=database
        )
        Logger.success("Connection to MySQL DB successful")
    except Error as e:
        Logger.error(f"The error '{e}' occurred")
    return connection


def get_company(connection, company_id):
    """
    Get company information by company ID.

    Args:
        connection (mysql.connector.connection.MySQLConnection): The database connection object.
        company_id (int): The company ID.

    Returns:
        list: A list of tuples containing company information.
    """
    query = f"SELECT * FROM company WHERE id={company_id}"
    cursor = connection.cursor()
    result = None

    try:
        cursor.execute(query)
        result = cursor.fetchall()
    except Error as e:
        Logger.error(f"The error '{e}' occurred")

    return result


def insert_data(connection, table, data, company_id):
    """
    Insert data into the specified table.

    Args:
        connection (mysql.connector.connection.MySQLConnection): The database connection object.
        table (str): The name of the table.
        data (list): A list of dictionaries containing the data to be inserted.
        company_id (int): The company ID to associate with the data.

    Returns:
        None
    """
    columns = ', '.join(data[0].keys())
    placeholders = ', '.join(['%s'] * len(data[0]))
    query = f"INSERT INTO {table} ({columns}, company_id) VALUES ({placeholders}, %s)"
    cursor = connection.cursor()

    try:
        for record in data:
            cursor.execute(query, tuple(record.values()) + (company_id,))
        connection.commit()
        Logger.success(
            f"{len(data)} records inserted successfully into {table} table")
    except Error as e:
        Logger.error(f"The error '{e}' occurred")
