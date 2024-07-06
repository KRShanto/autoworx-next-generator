import json
from data_generator import create_function

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

customer_functions = [create_function(
    "generate_customer", "Generate n amount random customers data", customer_properties)]


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
