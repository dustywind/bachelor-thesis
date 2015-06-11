
from . import TfIdfVector
from ..abstractvector import VectorCreatorFabric
from ..termfrequency import TermFrequencyVectorCreator
from ..inversedocumentfrequency import InverseDocumentFrequencyVectorCreator

class TfIdfVectorCreator(VectorCreatorFabric):
    
    def __init__(self, sqlite3_connection):
        super(TfIdfVectorCreator, self).__init__(sqlite3_connection)

        self.tf_creator = TermFrequencyVectorCreator(self._conn)
        self.idf_creator = InverseDocumentFrequencyVectorCreator(self._conn)
        pass

    def _create_vector(self, document_id):

        tf_vector = self.tf_creator.get_vector(document_id)
        idf_vector = self.idf_creator.get_vector(document_id)

        tfidf_vector = TfIdfVector()

        for triple in self._get_value_generator(tf_vector, idf_vector):
            tfidf_vector.add_to_vector(triple)

        return tfidf_vector

    def _get_value_generator(self, tfv, idfv):
        ingredients = zip(tfv.term_id, tfv.description, tfv.values, idfv.values)

        for (tf_tid, tf_desc, tf_val, idf_val) in ingredients:
            yield (tf_tid, tf_desc, tf_val * idf_val)
            pass
        pass
