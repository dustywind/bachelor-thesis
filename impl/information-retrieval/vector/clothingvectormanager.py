
from vectormanager import VectorManager
from vectortablecreator import VectorTableCreator
from tfidfvectorcreator import TfIdfVectorCreator

class ClothingVectorManager(VectorManager):

    def __init__(self, sqlite3_connection):
        self.__conn = sqlite3_connection
        self._tfidf_vector_creator = TfIdfVectorCreator()

        tablecreator = VectorTableCreator(self.__conn)
        tablecreator.init_database()

    def get_vector_for_documentid(self, document_id):
        return self._tfidf_vector_creator.create_vector(document_id)

    def get_all_vectors(self):
        raise NotImplementedError()
