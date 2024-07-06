import os
from openai import OpenAI
from dotenv import load_dotenv
from db_utils import create_connection, get_company, insert_data
from data_generator import generate_data
from logger import Logger
from models.customer import customer_functions, customer_messages
from models.vehicle import vehicle_functions, vehicle_messages
from models.vendor import vendor_functions, vendor_messages


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
