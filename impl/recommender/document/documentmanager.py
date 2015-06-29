
import sqlite3
import sys

from ..dependency import Dependency
from .documenttablecreator import  DocumentTableCreator

class DocumentManager(Dependency):
    """Creates a DocumentManager

    DocumentManager will call :func:`recommender.document.DocumentTableCreator.init_database`

    :param database_manager: instance of a DatabaseManager
    :type database_manager: recommender.DatabaseManager
    """

    def __init__(self, database_manager):
        super(DocumentManager, self).__init__(database_manager)
        self._conn = self._database_manager._conn

        table_creator = DocumentTableCreator(self._conn)
        table_creator.init_database()
        pass

    def build_dependencies(self):
        """There are no dependencies that have to be built

        Inherited from :class:`recommender.Dependencies`
        """
        pass

    def get_new_document_id(self):
        """Creates a new unique document_id by storing it in the database
        """
        try:
            self._add_document()
            return self._get_latest_document_id()
        except:
            raise Exception(sys.exc_info())
        pass

    def _add_document(self):
        """Adds a new Document into the database in order to generate a unique id

        The id can be queried by :func:`recommender.document.Document._get_lastest_id'
        """
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
        """Queries the last id inserted in the Database

        :returns: int representing a new document
        """
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
        """Checks whether the document_id is already in use or not.

        :param document_id: int representing a document
        :type document_id: int
        :returns: bool -- True, if the document does exists
        """
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









