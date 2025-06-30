import sqlite3
import os

def get_connection():
    """
    Establish and return a connection to the database using a relative path.
    """
    # Automatically find the database file based on the script's location
    db_path = os.path.join(os.path.dirname(__file__), "../db/cinema_booking.db")
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found at {db_path}")
    return sqlite3.connect(db_path)
