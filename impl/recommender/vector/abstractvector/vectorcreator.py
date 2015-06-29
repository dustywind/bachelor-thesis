

import sqlite3

class VectorCreator(object):
    """
    Abstract class that represents a VectorFabric

    .. warning::
        Do **not** directly initialize this class -- use inherited classes instead!

    :param sqlite3_connection: connection to a database build with :class:`recommender.vector.VectorTableCreator`
    :type sqlite3_connection: sqlite3.Connection
    :raises: TypeError
    """

    def __init__(self, sqlite3_connection):
        if not isinstance(sqlite3_connection, sqlite3.Connection):
            raise TypeError()
        self._conn = sqlite3_connection
        self._cache = {}
        pass

    def get_vector(self, document_id=None):
        """Get a vector that represents the data stored for the given document.
        
        .. note::
            This class buffers all vectors -- to clear the buffer use :func:`flush`

        :param document_id: the document_id of a document stored in the database
        :type document_id: int
        :returns: DocumentVector -- A vector representing the corresponding values from the database
        """
        if document_id is not None and not isinstance(document_id, int):
            raise TypeError('document_id must either be an integer or None')
        if not document_id in self._cache:
            self._cache[document_id] = self._create_vector(document_id)
        return self._cache[document_id]

    def _create_vector(self, document_id=None):
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
        del(self._cache)
        self._cache = {}
        pass

