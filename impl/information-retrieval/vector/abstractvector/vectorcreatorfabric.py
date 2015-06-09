

import sqlite3

class VectorCreatorFabric(object):

    def __init__(self, sqlite3_connection):
        if not isinstance(sqlite3_connection, sqlite3.Connection):
            raise TypeError()
        self._conn = sqlite3_connection
        pass

    def create_vector(self, document_id):
        raise NotImplementedError()
