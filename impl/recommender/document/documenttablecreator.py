
import os
import sqlite3
import sys

from .. import TableCreator

class DocumentTableCreator(TableCreator):
    """Creates all tables that are necessary to operate :class:`recommender.document.DocumentManager`

    :param sqlite3_connection: an open database connection
    :type sqlite3_connection: sqlite3.Connection
    """
    
    def __init__(self, db_connection_str):
        super(DocumentTableCreator, self).__init__(db_connection_str)
        pass

    def init_database(self):
        """Triggers the creation of all tables

        Overwrites :func:`recommender.TableCreator.init_database`
        """
        self._create_table_document()

    def _create_table_document(self):
        """Creates the Document-table, if it doesn't already exist
        """
        with self._get_db_connection() as conn:
            c = conn.cursor()
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
                conn.rollback()
                raise Exception(sys.exc_info())
            else:
                conn.commit()






