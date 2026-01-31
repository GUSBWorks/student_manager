import sqlite3
import os

# Updated database name based on your changes
DB_NAME = "students.db"

def get_db_connection():
    """
    Creates and returns a connection to the SQLite database.
    Sets row_factory to sqlite3.Row to access columns by name.
    """
    # Get the absolute path to ensure we find the DB file correctly
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level to app/database/ (or adjust depending on where the db file is)
    # Since we run from root, relative path usually works, but let's be safe:
    db_path = os.path.join(os.getcwd(), 'app', 'database', DB_NAME)
    
    # Fallback: if running directly inside database folder
    if not os.path.exists(os.path.dirname(db_path)):
        db_path = DB_NAME

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # This allows accessing data like dicts: row['email']
    return conn
