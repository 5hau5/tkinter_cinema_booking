from utils.database import get_connection

class BaseModel:
    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()
