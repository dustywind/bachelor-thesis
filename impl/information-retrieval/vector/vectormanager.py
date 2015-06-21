
import sqlite3

from ..dependency import Dependency

class VectorManager(Dependency):

    def __init__(self, database_manager):
        super(VectorManager, self).__init__(database_manager)

        self._database_manager = database_manager
        self._conn = self._database_manager._conn
        pass

    def build_dependencies(self):
        """inherited from Dependency
        """
        raise NotImplementedError()

    def get_vector_for_documentid(self, document_id):
        raise NotImplementedError()

    def get_all_vectors(self):
        raise NotImplementedError()
