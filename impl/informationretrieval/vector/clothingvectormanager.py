
from .vectormanager import VectorManager
from .vectortablecreator import VectorTableCreator

from .tfidf import TfIdfVectorCreator

class ClothingVectorManager(VectorManager):
    """Manages the Clothing-Vectors
    
    Inherits :class:`vector.vectormanager.VectorManager` 

    :param database_manager: 
    :type database_manager: DatabaseManager
    """

    def __init__(self, database_manager):
        super(ClothingVectorManager, self).__init__(database_manager)
        self._create_tables()
        self._tfidf_vector_creator = TfIdfVectorCreator(self._conn)
        pass

    def build_dependencies(self):
        """need tables built by ClothingManager
        """
        _ = self._database_manager.get_clothing_manager()
        pass

    def _create_tables(self):
        tablecreator = VectorTableCreator(self._conn)
        tablecreator.init_database()
        

    def get_vector_for_documentid(self, document_id):
        """Get the vector that represents the ``document_id``
        
        :param document_id: document_id that represents a document in the database
        :type document_id: int
        :returns: a ``TfIdfVector`` that resembles the document
        """
        return self._tfidf_vector_creator.create_vector(document_id)

    def get_all_vectors(self):
        raise NotImplementedError()
