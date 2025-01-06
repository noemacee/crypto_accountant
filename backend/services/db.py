import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv


def get_db_connection():
    """
    Establish and return a connection to the PostgreSQL database.
    Reads credentials from environment variables.
    """

    load_dotenv()
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL environment variable is not set.")

    try:
        conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        return conn
    except Exception as e:
        raise RuntimeError(f"Error connecting to the database: {e}")


def execute_query(query, params=None):
    """
    Execute a query on the database and return results as a dictionary.
    :param query: SQL query to execute.
    :param params: Optional parameters for the query.
    :return: Query results as a list of dictionaries (if SELECT) or None (if not SELECT).
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                if query.strip().lower().startswith("select"):
                    return cursor.fetchall()  # For SELECT queries, fetch results
                conn.commit()  # For INSERT/UPDATE/DELETE queries, commit changes
    except Exception as e:
        raise RuntimeError(f"Error executing query: {e}")


def execute_sql_file(file_path):
    """
    Execute an SQL file against the database.
    :param file_path: Path to the SQL file to execute.
    """
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                with open(file_path, "r") as f:
                    sql = f.read()
                    cursor.execute(sql)
                conn.commit()
    except Exception as e:
        raise RuntimeError(f"Error executing SQL file {file_path}: {e}")
