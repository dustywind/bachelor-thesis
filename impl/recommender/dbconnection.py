
import sqlite3

class DbConnection:

    def __init__(self, connection_str):
        self._conn = sqlite3.connect(connection_str)

    def __enter__(self):
        return self._conn

    def __exit__(self, type, value, traceback):
        if self._conn is not None:
            self._conn.close()
        pass



