
import sqlite3
import sys

from ..dependency import Dependency
from .documenttablecreator import  DocumentTableCreator

class DocumentManager(Dependency):

    def __init__(self, database_manager):
        super(DocumentManager, self).__init__(database_manager)
        self._conn = self._database_manager._conn

        table_creator = DocumentTableCreator(self._conn)
        table_creator.init_database()
        pass

    def build_dependencies(self):
        pass

    def get_new_document_id(self):

        try:
            self._add_document()
            return self._get_latest_document_id()
        except:
            
            raise Exception(sys.exc_info())
            pass


        raise NotImplementedError()
        pass

    def _add_document(self):
        c = self._conn.cursor()
        try:
            c.execute(
                '''
                INSERT INTO Document
                VALUES (null)
                ;
                '''
            )
        except Exception:
            self._conn.rollback()
            raise Exception(sys.exc_info())
        else:
            self._conn.commit()
        pass

    def _get_latest_document_id(self):
        c = self._conn.cursor()
        c.execute(
            '''
            SELECT
                MAX(document_id)
            FROM
                Document
            ;
            '''
        )
        result = c.fetchone()
        return None if result is None else result[0]

    def has_document(self, document_id):
        c = self._conn.curosor()
        c.execute(
            '''
            SELECT
                document_id
            FROM
                Document
            ;
            '''
        )
        return c.fetchone() is not None









