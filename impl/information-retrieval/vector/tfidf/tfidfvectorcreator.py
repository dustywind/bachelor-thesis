
from . import TfIdfVector
from ..abstractvector import VectorCreatorFabric
from ..termfrequency import TermFrequencyVectorCreator
from ..inversedocumentfrequency import InverseDocumentFrequencyVectorCreator

class TfIdfVectorCreator(VectorCreatorFabric):
    
    def __init__(self, sqlite3_connection):
        super(TfIdfVectorCreator, self).__init__(sqlite3_connectin)

        self.tf_creator = TermFrequencyVectorCreator(self.conn)
        self.idf_creator = InverseDocumentFrequencyVectorCreator(self.conn)
        pass

    def _create_vector(self, document_id):

        tf_vector = self.tf_creator.get_document(document_id)
        idf_vector = self.idf_creator.get_document(document_id)

        tfidf_vector = TfIdfVector()

        #code might run, but it's not tested yet
        generator = ( (tf_tid, tf_desc, tf_val * idf_val) for (tf_tid, tf_desc, tf_val, idf_val) in zip(tf_vector.term_id, tf_vector.description, tf_vector.values, idf_vector.values))
            pass
        tfidf_vector.add_to_vector()

        raise NotImplementedError()
        return tfidf
