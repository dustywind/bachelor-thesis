
import sqlite3
import sys
import pdb

from .. import TableCreator

class TermTableCreator(TableCreator):
    """some comment"""

    def __init__(self, sqlite3_connection):
        super(TermTableCreator, self).__init__(sqlite3_connection)
        pass

    def init_database(self):
        """Creates all tables needed for the vectormodule
        """
        try:
            # the order is somewhat important to guarantee
            # referential integrity
            self._create_term_table()
            self._create_termdocumentassigner_table()
            self._create_n_view()
        except:
            self._conn.rollback()
            raise Exception(sys.exc_info())
        else:
            self._conn.commit()


    def _create_term_table(self):
        c = self._conn.cursor()
        c.execute(
            '''
            CREATE TABLE IF NOT EXISTS Term
            (
                term_id     INTEGER PRIMARY KEY,
                name        TEXT UNIQUE NOT NULL
            )
            ;
            '''
        )
        pass

    def _create_termdocumentassigner_table(self):
        c = self._conn.cursor()
        c.execute(
            '''
            CREATE TABLE IF NOT EXISTS TermDocumentAssigner
            (
                term_id     INTEGER NOT NULL,
                document_id INTEGER NOT NULL,
                count       INTEGER NOT NULL,

                PRIMARY KEY(term_id, document_id),

                FOREIGN KEY(term_id) REFERENCES Term(term_id),
                FOREIGN KEY(document_id) REFERENCES Document(document_id)
            )
            ;
            '''
        )
        c.execute(
            '''
            CREATE INDEX IF NOT EXISTS
            term_document_assigner_index ON
            TermDocumentAssigner(document_id)
            ;
            '''
        )

    def _create_n_view(self):
        c = self._conn.cursor()
        c.execute(
            '''
            CREATE VIEW IF NOT EXISTS N AS
            SELECT
                (SELECT COUNT(*) FROM Document) AS document_count,
                (SELECT COUNT(*) FROM Term) AS term_count
            ;
            '''
        )
        pass

