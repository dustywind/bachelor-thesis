
from .vectormanager import VectorManager
from .vectortablecreator import VectorTableCreator

from .documentfrequency import DocumentFrequencyVectorCreator
from .termfrequency import TermFrequencyVectorCreator
from .tfidf import TfIdfVectorCreator
from .inversedocumentfrequency import InverseDocumentFrequencyVectorCreator

class ProductVectorManager(VectorManager):
    """Manages the Clothing-Vectors
    
    Inherits :class:`vector.vectormanager.VectorManager` 

    :param database_manager: 
    :type database_manager: DatabaseManager
    """

    def __init__(self, database_manager):
        super(ProductVectorManager, self).__init__(database_manager)

        tablecreator = VectorTableCreator(self._conn)
        tablecreator.init_database()

        self._standard_vector_creator = TfIdfVectorCreator(self._conn)
        pass

    def build_dependencies(self):
        """need tables built by ClothingManager
        """
        _ = self._database_manager.get_product_manager()
        pass

    def get_vector_for_document_id(self, document_id):
        """Get the vector that represents the ``document_id``
        
        :param document_id: document_id that represents a document in the database
        :type document_id: int
        :returns: a ``TfIdfVector`` that resembles the document
        """
        return self._standard_vector_creator.get_vector(document_id)

    def get_document_frequency_vector(self, document_id=None):
        return DocumentFrequencyVectorCreator(self._conn).get_vector(document_id)

    def get_term_frequency_vector(self, document_id):
        return TermFrequencyVectorCreator(self._conn).get_vector()

    def get_tfidf_vector(self, document_id):
        return TfIdfVectorCreator(self._conn).get_vector(document_id)

    def get_inverse_document_frequency_vector(self, document_id=None):
        return InverseDocumentFrequencyVectorCreator(self._conn).get_vector()

    def get_all_vectors(self):
        raise NotImplementedError()




