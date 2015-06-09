
import sqlite3

from ..abstractvector import VectorCreatorFabric
from . import TermFrequencyVector

class TermFrequencyVectorCreator(VectorCreatorFabric):

    def __init__(self, sqlite3_connection):
        super(self.__class__, self).__init__(sqlite3_connection)
        pass

    def create_vector(self, document_id):
        vector = TermFrequencyVector()
        for value in self._get_vector_values_from_db(document_id):
            vector.add_to_vector(value)
            pass
        return vector

    def _get_vector_values_from_db(self, document_id):
        vector_values = []
        c = self._conn.cursor()
        c.execute(
            '''
            SELECT      t.term_id,
                        t.name,
                        CASE WHEN   a.document_id IS NULL
                            THEN    0
                            ELSE    1
                        END AS term_weight
            FROM        Term AS t
                        LEFT OUTER JOIN
                        (
                            SELECT  term_id, document_id
                            FROM    TermDocumentAssigner
                            WHERE   document_id = :document_id
                        ) AS a ON t.term_id = a.term_id
            ORDER BY    t.term_id
            ;
            ''', {'document_id': document_id})
        for result in c.fetchall():
            vector_values.append((result[0], result[1], result[2]))
            pass
        return vector_values

