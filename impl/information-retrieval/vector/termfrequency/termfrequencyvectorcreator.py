
import sqlite3

from ..abstractvector import VectorCreatorFabric
from . import TermFrequencyVector

class TermFrequencyVectorCreator(VectorCreatorFabric):

    def __init__(self, sqlite3_connection):
        super(TermFrequencyVectorCreator, self).__init__(sqlite3_connection)
        pass

    def _create_vector(self, document_id):
        if not self._has_document(document_id):
            return None
        return self._create_vector_no_check(document_id)

    def _create_vector_no_check(self, document_id):
        vector = TermFrequencyVector()
        values = self._get_vector_values_from_db(document_id)

        for value in [] if values is None else values:
            vector.add_to_vector(value)
            pass
        return vector


    def _has_document(self, document_id):
        c = self._conn.cursor()
        c.execute(
            '''
            SELECT document_id
            FROM    Clothing
            WHERE   document_id = :document_id
            ''', {'document_id': document_id}
        )
        return c.fetchone() is not None

    def _get_vector_values_from_db(self, document_id):
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
        vector_values = []
        for result in c.fetchall():
            vector_values.append((result[0], result[1], result[2]))
            pass
        return None if not vector_values else vector_values