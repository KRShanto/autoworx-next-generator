import json
from data_generator import create_function

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

vendor_functions = [create_function(
    "generate_vendor", "Generate n amount random vendors data", vendor_properties)]


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
