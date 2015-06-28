
import os
import sqlite3
import sys

from .. import TableCreator
#from .. import TableCreator

class DocumentTableCreator(TableCreator):
    
    def __init__(self, sqlite3_connection):
        super(DocumentTableCreator, self).__init__(sqlite3_connection)
        pass

    def init_database(self):
        self._create_table_document()

    def _create_table_document(self):
        c = self._conn.cursor()
        try:
            c.execute(
                '''
                CREATE TABLE IF NOT EXISTS Document
                (
                    document_id     INTEGER PRIMARY KEY
                )
                ;
                '''
            )
        except Exception:
            self._conn.rollback()
            raise Exception(sys.exc_info())
        else:
            self._conn.commit()






