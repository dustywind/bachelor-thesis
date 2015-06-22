
import sqlite3

from .tablecreator import TableCreator

class UserTableCreator(TableCreator):

    def __init__(self, sqlite3_connection):
        if not isinstance(sqlite3_connection, sqlite3.Connection):
            raise TypeError("")
        self._conn = sqlite3_connection

    def init_database(self):
        self._create_user_table()
        pass

    def _create_user_table(self):
        c = self._conn.cursor()
        c.execute(
            '''
            CREATE TABLE IF NOT EXISTS UserManagement
            (
                user_id     INTEGER PRIMARY KEY,
                name        TEXT NOT NULL
            )
            ;
            '''
        )
        pass
