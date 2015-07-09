

from ..df import DocumentFrequencyVectorCreator
from . import InverseDocumentFrequencyVector

class InverseDocumentFrequencyVectorCreator(DocumentFrequencyVectorCreator):
    
    def __init__(self, db_connection_str):
        super(InverseDocumentFrequencyVectorCreator, self).__init__(db_connection_str)
        self._create_inverse_document_frequency_view()
        pass

    def _create_vector(self, document_id=None):
        vector = InverseDocumentFrequencyVector()
        
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            values = self._get_vector_values_from_db(cursor)
            for value in [] if values is None else values:
                vector.add_to_vector(value)
            return vector

    def _get_vector_values_from_db(self, c):
        c.execute(
            '''
            SELECT  term_id, name, count
            FROM    InverseDocumentFrequency
            ;
            ''')
        vector_values = []
        for result in c.fetchall():
            vector_values.append((result[0], result[1], result[2]))
            pass
        return None if not vector_values else vector_values
   
    def _create_inverse_document_frequency_view(self):
        with self._get_db_connection() as conn:
            c = conn.cursor()
            c.execute(
                '''
                CREATE VIEW IF NOT EXISTS InverseDocumentFrequency AS
                    SELECT      term_id,
                                name,
                                count / CAST ((SELECT document_count from N) AS REAL) AS count
                    FROM        DocumentFrequency
                    ORDER BY    term_id
                ;
                ''')
            pass
