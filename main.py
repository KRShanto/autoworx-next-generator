
import mysql.connector
from mysql.connector import Error
from urllib.parse import urlparse
import os
import time
from openai import OpenAI
from dotenv import load_dotenv
import json
from colorama import Fore, Style, init

# Initialize colorama for colored terminal output
init()


class Logger:
    """
    A simple logger class for printing colored messages to the console.
    """
    @staticmethod
    def info(message):
        print(Fore.BLUE + message + Style.RESET_ALL)

    @staticmethod
    def success(message):
        print(Fore.GREEN + message + Style.RESET_ALL)

    @staticmethod
    def error(message):
        print(Fore.RED + message + Style.RESET_ALL)


def create_function(name, description, properties):
    """
    Create a function definition for OpenAI API function calling.

    Args:
        name (str): The name of the function.
        description (str): A brief description of what the function does.
        properties (dict): A dictionary defining the properties of the function's parameters.

    Returns:
        dict: A dictionary representing the function definition.
    """
    return {
        "name": name,
        "description": description,
        "parameters": {
            "type": "object",
            "properties": {
                "data": {
                    "type": "array",
                    "description": f"Array of {name.split('_')[1]}s",
                    "items": {
                        "type": "object",
                        "properties": properties
                    }
                }
            }
        }
    }


# Define the properties for customer
customer_properties = {
    "first_name": {"type": "string", "description": "First name of the customer"},
    "last_name": {"type": "string", "description": "Last name of the customer"},
    "email": {"type": "string", "description": "Email of the customer"},
    "mobile": {"type": "string", "description": "Phone number of the customer"},
    "address": {"type": "string", "description": "Address of the customer"},
    "city": {"type": "string", "description": "City of the customer"},
    "state": {"type": "string", "description": "State of the customer"},
    "zip": {"type": "string", "description": "Zip code of the customer"}
}

# Define the properties for vehicle
vehicle_properties = {
    "make": {"type": "string", "description": "Make of the vehicle"},
    "model": {"type": "string", "description": "Model of the vehicle"},
    "year": {"type": "string", "description": "Year of the vehicle"},
    "vin": {"type": "string", "description": "VIN of the vehicle"},
    "submodel": {"type": "string", "description": "Submodel of the vehicle"},
    "type": {"type": "string", "description": "Type of the vehicle"},
    "transmission": {"type": "string", "description": "Transmission of the vehicle"},
    "engineSize": {"type": "string", "description": "Engine size of the vehicle"},
    "license": {"type": "string", "description": "License plate of the vehicle"},
    "notes": {"type": "string", "description": "Notes about the vehicle (optional)"}
}

# Define the properties for vendor
vendor_properties = {
    "name": {"type": "string", "description": "Name of the vendor"},
    "website": {"type": "string", "description": "Website of the vendor"},
    "email": {"type": "string", "description": "Email of the vendor"},
    "phone": {"type": "string", "description": "Phone number of the vendor"},
    "address": {"type": "string", "description": "Address of the vendor"},
    "city": {"type": "string", "description": "City of the vendor"},
    "state": {"type": "string", "description": "State of the vendor"},
    "zip": {"type": "string", "description": "Zip code of the vendor"},
    "companyName": {"type": "string", "description": "Name of the company the vendor is associated with"},
    "notes": {"type": "string", "description": "Notes about the vendor (optional)"}
}

# Generate function definitions for each type of data
customer_functions = [create_function(
    "generate_customer", "Generate n amount random customers data", customer_properties)]
vehicle_functions = [create_function(
    "generate_vehicle", "Generate n amount random vehicles data", vehicle_properties)]
vendor_functions = [create_function(
    "generate_vendor", "Generate n amount random vendors data", vendor_properties)]


def generate_data(client, entity, rows, functions, messages):
    """
    Generate random data using OpenAI API and retry if the generation fails.

    Args:
        client (OpenAI): The OpenAI client instance.
        entity (str): The type of data to generate (e.g., 'customer', 'vehicle', 'vendor').
        rows (int): The number of rows of data to generate.
        functions (list): The function definitions for the OpenAI API.
        messages (list): The message prompts for the OpenAI API.

    Returns:
        list: A list of generated data.
    """
    Logger.info(f"Generating {entity} data...")
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        functions=functions,
        function_call="auto",
    )
    json_response = json.loads(
        response.choices[0].message.function_call.arguments)
    if not json_response:
        Logger.error(f"Failed to generate {entity} data. Retrying...")
        time.sleep(5)
        return generate_data(client, entity, rows, functions, messages)
    else:
        Logger.success(f"Successfully generated {entity} data.")
        return json_response["data"]


def customer_messages(rows):
    """
    Generate message prompts for generating customer data.

    Args:
        rows (int): The number of rows of data to generate.

    Returns:
        list: A list of message prompts.
    """
    return [
        {"role": "system", "content": "You are a fake data generator. Call the function to generate random customers data. The data should be very random and unique."},
        {"role": "user", "content": f"Generate 2 rows of random customers data"},
        {
            "role": "function",
            "name": "generate_customer",
            "content": json.dumps({
                "data": [
                    {
                        "first_name": "John",
                        "last_name": "Doe",
                        "email": "johndoe@gmail.com",
                        "mobile": "1234567890",
                        "address": "123 Main St",
                        "city": "New York",
                        "state": "NY",
                        "zip": "10001"
                    },
                    {
                        "first_name": "Jane",
                        "last_name": "Smith",
                        "email": "janesmith@hotmail.com",
                        "mobile": "0987654321",
                        "address": "456 Elm St",
                        "city": "Los Angeles",
                        "state": "CA",
                        "zip": "90001"
                    }
                ]
            })
        },
        {
            "role": "user",
            "content": "Generate 4 rows of random customers data",
        },
        {
            "role": "function",
            "name": "generate_customer",
            "content": json.dumps({
                "data": [
                    {
                        "first_name": "Alice",
                        "last_name": "Johnson",
                        "email": "alicejohnson@example.com",
                        "mobile": "98765222210",
                        "address": "789 Oak St",
                        "city": "Chicago",
                        "state": "IL",
                        "zip": "60007"
                    },
                    {
                        "first_name": "Bob",
                        "last_name": "Brown",
                        "email": "bobbrown@ext.com",
                        "mobile": "1234567890",
                        "address": "123 Main St",
                        "city": "New York",
                        "state": "NY",
                        "zip": "10001"
                    },
                    {
                        "first_name": "Charlie",
                        "last_name": "White",
                        "email": "charlie@white.com",
                        "mobile": "0117654321",
                        "address": "New York, USA",
                        "city": "New York",
                        "state": "NY",
                        "zip": "10001"
                    },
                    {
                        "first_name": "David",
                        "last_name": "Smith",
                        "email": "david3005@british.ca",
                        "mobile": "1234567890",
                        "address": "123 Burnaby, BC",
                        "city": "Vancouver",
                        "state": "BC",
                        "zip": "V5G 1C7"
                    }
                ]
            })
        },
        {
            "role": "user",
            "content": f"Generate {rows} row of random customers data",
        }
    ]


def vehicle_messages(rows):
    """
    Generate message prompts for generating vehicle data.

    Args:
        rows (int): The number of rows of data to generate.

    Returns:
        list: A list of message prompts.
    """
    return [
        {"role": "system", "content": "You are a fake data generator. Call the function to generate random vehicles data. The data should be very random and unique."},
        {"role": "user", "content": f"Generate 2 rows of random vehicles data"},
        {
            "role": "function",
            "name": "generate_vehicle",
            "content": json.dumps({
                "data": [
                    {
                        "make": "Toyota",
                        "model": "Corolla",
                        "year": "2019",
                        "vin": "1G1BE5SMXG7300001",
                        "submodel": "LE",
                        "type": "Sedan",
                        "transmission": "Automatic",
                        "engineSize": "1.8L",
                        "license": "ABC123",
                        "notes": "No accidents"
                    },
                    {
                        "make": "Ford",
                        "model": "F-150",
                        "year": "2020",
                        "vin": "1G1BE5SMXG7300002",
                        "submodel": "XLT",
                        "type": "Truck",
                        "transmission": "Automatic",
                        "engineSize": "5.0L",
                        "license": "DEF456",
                        "notes": "Minor scratches on the rear bumper"
                    }
                ]
            })
        },
        {
            "role": "user",
            "content": "Generate 4 rows of random vehicles data",
        },
        {
            "role": "function",
            "name": "generate_vehicle",
            "content": json.dumps({
                "data": [
                    {
                        "make": "Honda",
                        "model": "Civic",
                        "year": "2018",
                        "vin": "1G1BE5SMXG7300003",
                        "submodel": "EX",
                        "type": "Sedan",
                        "transmission": "Automatic",
                        "engineSize": "2.0L",
                        "license": "GHI789",
                        "notes": "Well maintained"
                    },
                    {
                        "make": "Chevrolet",
                        "model": "Equinox",
                        "year": "2017",
                        "vin": "1G1BE5SMXG7300004",
                        "submodel": "LT",
                        "type": "SUV",
                        "transmission": "Automatic",
                        "engineSize": "2.4L",
                        "license": "JKL012",
                        "notes": "New tires"
                    },
                    {
                        "make": "Nissan",
                        "model": "Altima",
                        "year": "2016",
                        "vin": "1G1BE5SMXG7300005",
                        "submodel": "SL",
                        "type": "Sedan",
                        "transmission": "Automatic",
                        "engineSize": "2.5L",
                        "license": "MNO345",
                        "notes": "One owner"
                    },
                    {
                        "make": "Toyota",
                        "model": "Sienna",
                        "year": "2015",
                        "vin": "1G1BE5SMXG7300006",
                        "submodel": "LE",
                        "type": "Minivan",
                        "transmission": "Automatic",
                        "engineSize": "3.5L",
                        "license": "PQR678",
                        "notes": "No accidents"
                    }
                ]
            })
        },
        {
            "role": "user",
            "content": f"Generate {rows} row of random vehicles data",
        }
    ]


def vendor_messages(rows):
    """
    Generate message prompts for generating vendor data.

    Args:
        rows (int): The number of rows of data to generate.

    Returns:
        list: A list of message prompts.
    """
    return [
        {"role": "system", "content": "You are a fake data generator. Call the function to generate random vendors data. The data should be very random and unique."},
        {"role": "user", "content": f"Generate 2 rows of random vendors data"},
        {
            "role": "function",
            "name": "generate_vendor",
            "content": json.dumps({
                "data": [
                    {
                        "name": "Rohan Motors",
                        "website": "https://abcinc.com",
                        "email": "rohan@gmail.om",
                        "phone": "1234567890",
                        "address": "123 Main St",
                        "city": "New York",
                        "state": "NY",
                        "zip": "10001",
                        "companyName": "ABC Inc",
                        "notes": "No accidents"
                    },
                    {
                        "name": "John Doe",
                        "website": "https://xyzinc.com",
                        "email": "johndoe@xyz.com",
                        "phone": "0987654321",
                        "address": "456 Elm St",
                        "city": "Los Angeles",
                        "state": "CA",
                        "zip": "90001",
                        "companyName": "XYZ Inc",
                        "notes": "Minor scratches on the rear bumper"
                    }
                ]
            })
        },
        {
            "role": "user",
            "content": "Generate 4 rows of random vendors data",
        },
        {
            "role": "function",
            "name": "generate_vendor",
            "content": json.dumps({
                "data": [
                    {
                        "name": "Alice Johnson",
                        "website": "https://alicejohnson.com",
                        "email": "alicejohnson@example.com",
                        "phone": "98765222210",
                        "address": "789 Oak St",
                        "city": "Chicago",
                        "state": "IL",
                        "zip": "60007",
                        "companyName": "Alice Corp",
                        "notes": "Well maintained"
                    },
                    {
                        "name": "Bob Brown",
                        "website": "https://bobbrown.com",
                        "email": "bobbrown@ext.com",
                        "phone": "1234567890",
                        "address": "123 Main St",
                        "city": "New York",
                        "state": "NY",
                        "zip": "10001",
                        "companyName": "Bob Corp",
                        "notes": "New tires"
                    },
                    {
                        "name": "Charlie White",
                        "website": "https://charliewhite.com",
                        "email": "charlie@white.com",
                        "phone": "0117654321",
                        "address": "New York, USA",
                        "city": "New York",
                        "state": "NY",
                        "zip": "10001",
                        "companyName": "Mark Factory",
                        "notes": ""
                    },
                    {
                        "name": "David Smith",
                        "website": "https://chicagogrand.com",
                        "email": "david3005@gmail.in",
                        "phone": "1234522290",
                        "address": "123 Burnaby, BC",
                        "city": "Vancouver",
                        "state": "BC",
                        "zip": "V5G 1C7",
                        "companyName": "Chicago Grand Avenue",
                        "notes": ""
                    }
                ]
            })
        },
        {
            "role": "user",
            "content": f"Generate {rows} row of random vendors data",
        }
    ]


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


def main():
    """
    Main function to execute the script.

    Loads environment variables, creates database connection, generates data, 
    and inserts the data into the database.

    Args:
        None

    Returns:
        None
    """
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    db_url = os.getenv("DATABASE_URL")

    client = OpenAI(api_key=api_key)
    connection = create_connection(db_url)

    rows = input(
        "How many rows of data do you want to generate? (default is 5): ")
    if not rows:
        rows = 5
    else:
        rows = int(rows)
    if rows < 1:
        Logger.error("Invalid number of rows. Program will now exit.")
        exit(1)

    company_id = int(input("Enter the company id: "))

    company_info = get_company(connection, company_id)

    if not company_info:
        Logger.error("Company not found. Program will now exit.")
        exit(1)
    else:
        Logger.success(f"Company found: {company_info[0][1]}")

    customers = generate_data(client, 'customer', rows,
                              customer_functions, customer_messages(rows))
    vehicles = generate_data(client, 'vehicle', rows,
                             vehicle_functions, vehicle_messages(rows))
    vendors = generate_data(client, 'vendor', rows,
                            vendor_functions, vendor_messages(rows))

    # Insert the data into the database
    insert_data(connection, 'customer', customers, company_id)
    insert_data(connection, 'vehicle', vehicles, company_id)
    insert_data(connection, 'vendor', vendors, company_id)

    connection.close()


if __name__ == "__main__":
    main()
