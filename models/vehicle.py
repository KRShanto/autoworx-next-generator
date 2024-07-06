import json
from data_generator import create_function

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

vehicle_functions = [create_function(
    "generate_vehicle", "Generate n amount random vehicles data", vehicle_properties)]


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
