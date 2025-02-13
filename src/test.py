import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv  # Import dotenv to load environment variables

# Load environment variables from .env file
load_dotenv()

try:
    # Get credentials from .env
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        database=os.getenv('DB_NAME')
    )

    if conn.is_connected():
        print("Successfully connected to the database!")
    
    conn.close()

except Error as e:
    print(f"Error connecting to the database: {e}")
