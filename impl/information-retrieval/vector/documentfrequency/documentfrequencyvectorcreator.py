

from ..abstractvector import VectorCreatorFabric
from . import DocumentFrequencyVector

class DocumentFrequencyVectorCreator(VectorCreatorFabric):
    
    def __init__(self, sqlite3_connection):
        super(DocumentFrequencyVectorCreator, self).__init__(sqlite3_connection)
        self._create_document_frequency_view()
        pass

    def create_vector(self, document_id=None):
        vector = DocumentFrequencyVector()
        
        values = self._get_vector_values_from_db()
        for value in [] if values is None else values:
            vector.add_to_vector(value)
        return vector

    def _get_vector_values_from_db(self):
        c = self._conn.cursor()
        c.execute(
            '''
            SELECT  term_id, name, count
            FROM    DocumentFrequency
            ;
            ''')
        vector_values = []
        for result in c.fetchall():
            vector_values.append((result[0], result[1], result[2]))
            pass
        return None if not vector_values else vector_values
   
    def _create_document_frequency_view(self):
        c = self._conn.cursor()
        c.execute(
            '''
            CREATE VIEW IF NOT EXISTS DocumentFrequency AS
                SELECT      t.term_id,
                            t.name,
                            CASE WHEN   a.count IS NULL
                                THEN        0
                                ELSE        a.count
                            END AS count
                FROM        Term as t
                            LEFT OUTER JOIN
                            (
                                SELECT      term_id, COUNT(document_id) AS count
                                FROM        TermDocumentAssigner
                                GROUP BY    term_id
                            ) AS a ON t.term_id = a.term_id
                    ORDER BY    t.term_id
            ;
            ''')
        pass


