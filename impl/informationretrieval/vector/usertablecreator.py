
import sqlite3
import sys

from .. import TableCreator

class UserTableCreator(TableCreator):

    def __init__(self, sqlite3_connection):
        super(UserTableCreator, self).__init__(sqlite3_connection)
        pass

    def init_database(self):
        try:
            self._create_tables()
        except Exception:
            self._conn.rollback()
            raise Exception(sys.exc_info())
        else:
            self._conn.commit()

    def _create_tables(self):
        self._create_usermanagement_table()
        self._create_uservector_table()
        self._create_userpreference_table()
        pass
        
    def _create_usermanagement_table(self):
        c = self._conn.cursor()
        c.execute(
            '''
            CREATE TABLE IF NOT EXISTS UserManagement
            (
                user_id     INTEGER PRIMARY KEY,
                name        TEXT UNIQUE NOT NULL
            )
            ;
            '''
        )
        pass

    def _create_uservector_table(self):
        c = self._conn.cursor()
        c.execute(
            '''
            CREATE TABLE IF NOT EXISTS UserVector
            (
                user_id     INTEGER NOT NULL,
                term_id     INTEGER NOT NULL,
                value       REAL NOT NULL,

                PRIMARY KEY(user_id, term_id),

                FOREIGN KEY(term_id) REFERENCES Term(term_id),
                FOREIGN KEY(user_id) REFERENCES UserManagement(user_id)
            );
            '''
        )
        pass

    def _create_userpreference_table(self):
        c = self._conn.cursor()
        c.execute(
            '''
            CREATE TABLE IF NOT EXISTS UserPreference
            (
                user_id     INTEGER NOT NULL,
                document_id INTEGER NOT NULL,

                PRIMARY KEY(user_id, document_id),

                FOREIGN KEY(user_id) REFERENCES UserManagement(user_id),
                FOREIGN KEY(document_id) REFERENCES Clothing(document_id)
            )
            ;
            '''
        )
        pass



