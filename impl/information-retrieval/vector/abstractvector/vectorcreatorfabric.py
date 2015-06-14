
"""
.. module:: vectorcreatorfabric
    :synopsis: abstract base class for VectorCreators
"""


import sqlite3

class VectorCreatorFabric(object):
    """
    Abstract class that represents a VectorFabric

    .. warning::
        Do **not** directly initialize this class -- use inherited classes instead!
    """

    def __init__(self, sqlite3_connection):
        """
        :param sqlite3_connection: connection to a database build with :class:`vector.vectortablecreator.VectorTableCreator`
        :type sqlite3_connection: sqlite3.Connection
        """
        if not isinstance(sqlite3_connection, sqlite3.Connection):
            raise TypeError()
        self._conn = sqlite3_connection
        self.cache = {}
        pass

    def get_vector(self, document_id):
        """Get a vector that represents the data stored for the given document.
        
        .. note::
            This class buffers all vectors -- to clear the buffer use :func:`flush`

        :param document_id: the document_id of a document stored in the database
        :type document_id: int
        :returns: DocumentVector -- A vector representing the corresponding values from the database
        """
        if not self.cache.has_key(document_id):
            self.cache[document_id] = self._create_vector(document_id)
        return self.cache[document_id]

    def _create_vector(self, document_id):
        """Creates a vector that represents the document identified by the document_id
        :param document_id: the document id for a document
        :type document_id: int
        :returns: DocumentVector -- a Vector that represents the data stored for the given document_id

        .. warning::
            This is an abstract method -- do **not** use it
        """
        raise NotImplementedError()

    def flush(self):
        """Removes all buffered vectors.
        """
        del(self.cache)
        self.cache = {}
        pass

