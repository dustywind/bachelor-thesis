
import sqlite3

class VectorManager(object):

    def __init__(self, sqlite3_connection):
        if not isinstance(sqlite3_connection, sqlite3.Connection):
            raise TypeError('Needs an instance of sqlite3.Connection')
        self._conn = sqlite3_connection
        pass

    def get_vector_for_documentid(self, document_id):
        raise NotImplementedError()

    def get_all_vectors(self):
        raise NotImplementedError()
