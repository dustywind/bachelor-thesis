
import sqlite3
import sys

from irdb import TableCreator

class VectorTableCreator(TableCreator):

    def __init__(self, conn):
        self.__conn = conn

    def init_database(self):
        try:
            self.__create_term_table()
            self.__create_termdocumentassigner_table()
            self.__create_n_view()
        except Exception:
            self.__conn.rollback()
            raise Exception(sys.exc_info())
        else:
            self.__conn.commit()

    def __create_term_table(self):
        c = self.__conn.cursor()
        c.execute(
            '''
            CREATE TABLE IF NOT EXISTS Term
            (
                term_id     INTEGER PRIMARY KEY,
                value       TEXT UNIQUE NOT NULL
            );
            '''
        )

    def __create_termdocumentassigner_table(self):
        c = self.__conn.cursor()
        c.execute(
            '''
            CREATE TABLE IF NOT EXISTS TermDocumentAssigner
            (
                term_id     INTEGER,
                document_id INTEGER,

                PRIMARY KEY(term_id, document_id),

                FOREIGN KEY(term_id) REFERENCES Term(term_id),
                FOREIGN KEY(document_id) REFERENCES Clothing(document_id)
            )
            '''
        )
        c.execute(
            '''
            CREATE INDEX IF NOT EXISTS
            term_document_assigner_index ON
            TermDocumentAssigner(document_id)
            '''
        )
        

    def __create_n_view(self):
        c = self.__conn.cursor()
        c.execute(
            '''
            CREATE VIEW IF NOT EXISTS N AS
            SELECT      COUNT(*) AS n
            FROM        Clothing;
            '''
        )
