import json
import os
import time
from logger import Logger


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

    # get model from .env
    model = os.getenv("OPENAI_MODEL")
    if not model:
        model = "gpt-3.5-turbo"

    Logger.info(f"Generating {entity} data...")
    response = client.chat.completions.create(
        model=model,
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
