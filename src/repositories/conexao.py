import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    conn_str = (
        f"Driver={{{os.getenv('DB_DRIVER')}}};"
        f"Server={os.getenv('DB_SERVER')};"
        f"Database={os.getenv('DB_DATABASE')};"
        f"Trusted_Connection={os.getenv('DB_TRUSTED_CONNECTION')};"
    )

    return pyodbc.connect(conn_str, timeout=0)