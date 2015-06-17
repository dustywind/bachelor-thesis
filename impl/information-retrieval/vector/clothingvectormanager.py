
from .vectormanager import VectorManager
from .vectortablecreator import VectorTableCreator

from .tfidf import TfIdfVectorCreator

class ClothingVectorManager(VectorManager):

    def __init__(self, sqlite3_connection):
        super(ClothingVectorManager, self).__init__(sqlite3_connection)

        tablecreator = VectorTableCreator(self._conn)
        tablecreator.init_database()

        self._tfidf_vector_creator = TfIdfVectorCreator(self._conn)
        pass

    def get_vector_for_documentid(self, document_id):
        return self._tfidf_vector_creator.create_vector(document_id)

    def get_all_vectors(self):
        raise NotImplementedError()
