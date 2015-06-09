

#from termfrequencyvector import TermFrequencyVector
#from vectorcreatorfabric import VectorCreatorFabric
from ..abstractvector import VectorCreatorFabric

class TermFrequencyVectorCreator(VectorCreatorFabric):

    def __init__(self, sqlite3_connection):
        pass

    def create_vector(document_id):
        raise NotImplementedError()

    def _get_vector_values_from_db(document_id):
        
        raise NotImplementedError

