

class ClothingVectorManager(VectorManager):

    def __init__(self, sqlite3_connection):
        self.__conn = sqlite3_connection

    def get_vector_for_documentid(self, document_id):
        raise NotImplementedError()

    def get_all_vectors(self):
        raise NotImplementedError()
