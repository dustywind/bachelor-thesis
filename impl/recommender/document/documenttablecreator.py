
import os
import sqlite3
import sys

from .. import TableCreator

class DocumentTableCreator(TableCreator):
    """Creates all tables that are necessary to operate :class:`recommender.document.DocumentManager`

    :param sqlite3_connection: an open database connection
    :type sqlite3_connection: sqlite3.Connection
    """
    
    def __init__(self, sqlite3_connection):
        super(DocumentTableCreator, self).__init__(sqlite3_connection)
        pass

    def init_database(self):
        """Triggers the creation of all tables

        Overwrites :func:`recommender.TableCreator.init_database`
        """
        self._create_table_document()

    def _create_table_document(self):
        """Creates the Document-table, if it doesn't already exist
        """
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






