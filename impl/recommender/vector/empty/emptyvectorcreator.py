

from . import EmptyVector
from ..abstractvector import VectorCreator

class EmptyVectorCreator(VectorCreator):
    """Creates empty vectors

    Inherits from :class:`recommender.vector.abstractvector.VectorCreatorFabric`

    :parameter sqlite3_connection: connection to a database vuild with :class:`recommender.vector.vectortablecreator.VectorTableCreator`
    :type sqlite3_connection: sqlite3.Connection
    :raises: TypeError
    """
    
    def __init__(self, db_connection_str):
        super(EmptyVectorCreator, self).__init__(db_connection_str)
        pass

    def get_vector(self, document_id=None):
        """gets an empty vector

        :returns: :class:`recommender.vector.empty.EmptyVector` -- an empty vector
        """
        return self._create_vector()

    def _create_vector(self):
        """creates an empty vector

        :returns: :class:`recommender.vector.empty.EmptyVector` -- an empty vector
        """
        with self._get_db_connection() as conn:
            c = conn.cursor()
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

