
import sqlite3

from ..dependency import Dependency
from ..dbconnection import DbConnection

class VectorManager(Dependency):

    def __init__(self, database_manager):
        super(VectorManager, self).__init__(database_manager)
        self._db_connection_str = database_manager.get_db_connection_str()
        pass

    def build_dependencies(self):
        """inherited from Dependency
        """
        raise NotImplementedError()

    def _get_db_connection(self):
        return DbConnection(self._db_connection_str)

    def get_vector_for_documentid(self, document_id):
        raise NotImplementedError()

    def get_all_vectors(self):
        raise NotImplementedError()
