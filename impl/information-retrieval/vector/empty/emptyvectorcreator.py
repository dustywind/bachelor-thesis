

from . import EmptyVector
from ..abstractvector import VectorCreatorFabric

class EmptyVectorCreator(VectorCreatorFabric):
    
    def __init__(self, sqlite3_connection):
        super(EmptyVectorCreator, self).__init__(sqlite3_connection)
        pass

    def _create_vector(self, document_id=None):
        c = self._conn.cursor()
        c.execute('''
            SELECT      term_id
                        , name
                        , 0 AS value
            FROM        Term
            ORDER BY    term_id
            ;
            ''')
        vector = EmptyVector()
        for triple in c.fetchall():
            vector.add_to_vector(triple)
        return vector
        pass

