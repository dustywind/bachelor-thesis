
import sqlite3
import sys

from .. import TableCreator

class UserTableCreator(TableCreator):

    def __init__(self, db_connection_str):
        super(UserTableCreator, self).__init__(db_connection_str)
        pass

    def init_database(self):
        with self._get_db_connection() as conn:
            try:
                cursor = conn.cursor()
                self._create_tables(cursor)
            except Exception:
                conn.rollback()
                raise Exception(sys.exc_info())
            else:
                conn.commit()

    def _create_tables(self, cursor):
        self._create_usermanagement_table(cursor)
        self._create_uservector_table(cursor)
        self._create_userpreference_table(cursor)
        pass
        
    def _create_usermanagement_table(self, c):
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

    def _create_uservector_table(self, c):
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

    def _create_userpreference_table(self, c):
        c.execute(
            '''
            CREATE TABLE IF NOT EXISTS UserPreference
            (
                user_id     INTEGER NOT NULL,
                document_id INTEGER NOT NULL,

                PRIMARY KEY(user_id, document_id),

                FOREIGN KEY(user_id) REFERENCES UserManagement(user_id),
                FOREIGN KEY(document_id) REFERENCES Document(document_id)
            )
            ;
            '''
        )
        pass



