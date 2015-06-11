
"""
.. module:: vectorcreatorfabric
    :synopsis: abstract base class for VectorCreators
"""


import sqlite3

class VectorCreatorFabric(object):
    """
    Abstract class that represents a VectorFabric
    Vectors should be created with a VectorFabric
    """

    def __init__(self, sqlite3_connection):
        if not isinstance(sqlite3_connection, sqlite3.Connection):
            raise TypeError()
        self._conn = sqlite3_connection
        self.cache = {}
        pass

    def get_vector(self, document_id):
        """
        x.get_vector(self, document_id) -> DocumentVector -- either returns a buffered vector or creates a new one (depending on former queries) that represents the document identified by document_id
        """
        if not self.cache.has_key(document_id):
            self.cache[document_id] = self._create_vector(document_id)
        return self.cache[document_id]

    def _create_vector(self, document_id):
        """
        x._create_vector(self, document_id) -> DocumentVector -- creates a vector that represents the document identified by the document_id
        """
        raise NotImplementedError()

    def flush(self):
        """
        x.flush(self) -- removes all buffered vectors.
        """
        del(self.cache)
        self.cache = {}
        pass

