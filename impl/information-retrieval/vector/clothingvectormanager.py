
from .vectormanager import VectorManager
from .vectortablecreator import VectorTableCreator

from .tfidf import TfIdfVectorCreator

class ClothingVectorManager(VectorManager):
    """Manages the Clothing-Vectors
    
    Inherits :class:`vector.vectormanager.VectorManager` 

    :param sqlite3_connection: database connection where all the necessary tables are
    :type sqlite3_connection: sqlite3.Connection
    """

    def __init__(self, sqlite3_connection):
        super(ClothingVectorManager, self).__init__(sqlite3_connection)

        tablecreator = VectorTableCreator(self._conn)
        tablecreator.init_database()

        self._tfidf_vector_creator = TfIdfVectorCreator(self._conn)
        pass

    def get_vector_for_documentid(self, document_id):
        """Get the vector that represents the ``document_id``
        
        :param document_id: document_id that represents a document in the database
        :type document_id: int
        :returns: a ``TfIdfVector`` that resembles the document
        """
        return self._tfidf_vector_creator.create_vector(document_id)

    def get_all_vectors(self):
        raise NotImplementedError()
