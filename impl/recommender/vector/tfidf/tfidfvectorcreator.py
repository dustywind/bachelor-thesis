
from . import TfIdfVector
from ..abstractvector import VectorCreator
from ..tf import TermFrequencyVectorCreator
from ..idf import InverseDocumentFrequencyVectorCreator

class TfIdfVectorCreator(VectorCreator):
    
    def __init__(self, sqlite3_connection):
        super(TfIdfVectorCreator, self).__init__(sqlite3_connection)

        self._tf_creator = TermFrequencyVectorCreator(self._conn)
        self._idf_creator = InverseDocumentFrequencyVectorCreator(self._conn)
        pass

    def _create_vector(self, document_id):
        """

        called by :func:`recommender.vector.abstractvector.vectorcreatorfabric.VectorCreatorFabric`

        :param document_id: the document_id that resembles a document whose vector shall be built
        :type document_id: int
        :returns: an :class:`recommender.vector.tfidf.tfidfvector.TfIdfVector`
        """

        tf_vector = self._tf_creator.get_vector(document_id)
        idf_vector = self._idf_creator.get_vector(document_id)

        tfidf_vector = TfIdfVector()

        for triple in self._get_values(tf_vector, idf_vector):
            tfidf_vector.add_to_vector(triple)

        return tfidf_vector

    def _get_values(self, tfv, idfv):
        """Calculates the tf-idf-values from a TermFrequency- and a InverseDocumentFrequencyVector

        :param tfv: a term-frequency vector
        :type tfv: :class:`recommender.vector.tf.termfrequencyvector.TermFrequencyVector`
        :param idfv: a inverse-documentfrequency vector
        :type idfv: :class:`recommender.vector.idf.inversedocumentfrequencyvector.InverseDocumentFrequencyVector`
        """
        ingredients = zip(tfv.term_id, tfv.description, tfv.values, idfv.values)

        for (tf_tid, tf_desc, tf_val, idf_val) in ingredients:
            yield (tf_tid, tf_desc, tf_val * idf_val)
            pass
        pass
