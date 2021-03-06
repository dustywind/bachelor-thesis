
import os
import sqlite3
import sys

from .. import TableCreator

class ProductTableCreator(TableCreator):
    """
    Creates tables as defined in /docs/information_retrieval/ir_info
    """

    def __init__(self, db_connection_str):
        super(ProductTableCreator, self).__init__(db_connection_str)
        pass

    def init_database(self):
        self._create_table_product()

    def _create_table_product(self):
        with self._get_db_connection() as conn:
            c = conn.cursor()
            try:
                c.execute(
                    '''
                    CREATE TABLE IF NOT EXISTS Product
                    (
                        document_id     INTEGER,
                        image_name      TEXT UNIQUE NOT NULL,

                        PRIMARY KEY(document_id),

                        FOREIGN KEY(document_id) REFERENCES Document(document_id)
                    )
                    ;
                    '''
                )
            except Exception:
                conn.rollback()
                raise Exception(sys.exc_info())
            else:
                conn.commit()


