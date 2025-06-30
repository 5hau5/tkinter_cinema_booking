import sqlite3

class QueryHelper:
    def __init__(self, db_path='./db/cinema_booking.db'):
        """
        Initialize the QueryHelper with a connection to the database.
        """
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def add_row(self, table, data):
        """
        Adds a new row to the specified table.
        
        Parameters:
        - table (str): The table name.
        - data (dict): A dictionary of column names and their values.
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        values = tuple(data.values())
        
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(query, values)
        self.conn.commit()

    def remove_row(self, table, row_id):
        """
        Removes a row from the specified table based on its id.
        
        Parameters:
        - table (str): The table name.
        - row_id (int): The id of the row to remove.
        """
        query = f"DELETE FROM {table} WHERE id = ?"
        self.cursor.execute(query, (row_id,))
        self.conn.commit()

    def update_field(self, table, row_id, field, new_value):
        """
        Updates a specific field in a specified table for a given row.
        
        Parameters:
        - table (str): The table name.
        - row_id (int): The id of the row to update.
        - field (str): The field (column) to update.
        - new_value: The new value to set for the field.
        """
        query = f"UPDATE {table} SET {field} = ? WHERE id = ?"
        self.cursor.execute(query, (new_value, row_id))
        self.conn.commit()

    def close(self):
        """
        Closes the database connection.
        """
        self.conn.close()
