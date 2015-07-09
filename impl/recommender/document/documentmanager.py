
import sqlite3
import sys

from ..dependency import Dependency
from .. import DbConnection
from .documenttablecreator import  DocumentTableCreator

class DocumentManager(Dependency):
    """Creates a DocumentManager

    DocumentManager will call :func:`recommender.document.DocumentTableCreator.init_database`

    :param database_manager: instance of a DatabaseManager
    :type database_manager: recommender.DatabaseManager
    """

    def __init__(self, database_manager):
        super(DocumentManager, self).__init__(database_manager)
        self._db_connection_str = database_manager.get_db_connection_str()

        table_creator = DocumentTableCreator(self._db_connection_str)
        table_creator.init_database()

        self.temp_conn = None
        pass

    def _get_db_connection(self):
        if self.temp_conn is None:
            return DbConnection(self._db_connection_str)
        else:
            return self.temp_conn

    def build_dependencies(self):
        """There are no dependencies that have to be built

        Inherited from :class:`recommender.Dependencies`
        """
        pass

    def get_new_document_id(self):
        """Creates a new unique document_id by storing it in the database
        """
        doc_id = None
        with self._get_db_connection() as conn:
            try:
                self._add_document(conn)
                doc_id = self._get_latest_document_id(conn)
            except:
                conn.rollback()
                raise Exception(sys.exc_info())
            else:
                conn.commit()
                return doc_id
        pass

    def _add_document(self, conn):
        """Adds a new Document into the database in order to generate a unique id

        The id can be queried by :func:`recommender.document.Document._get_lastest_id'
        """
        c = conn.cursor()
        c.execute(
            '''
            INSERT INTO Document
            VALUES (null)
            ;
            '''
        )
        pass

    def _get_latest_document_id(self, conn):
        """Queries the last id inserted in the Database

        :returns: int representing a new document
        """
        c = conn.cursor()
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
        """Checks whether the document_id is already in use or not.

        :param document_id: int representing a document
        :type document_id: int
        :returns: bool -- True, if the document does exists
        """
        with self._get_db_connection() as conn:
            c = conn.curosor()
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









