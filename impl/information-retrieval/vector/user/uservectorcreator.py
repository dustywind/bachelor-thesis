
import sqlite3

from ..abstractvector import VectorCreatorFabric
from ..empty import EmptyVectorCreator

class UserVectorCreator(VectorCreatorFabric):
    
    def __init__(self, sqlite3_connection):
       super(UserVectorCreator, self).__init__(sqlite3_connection)
       self._empty_creator = EmptyVectorCreator(sqlite3_connection)
       pass

    def get_vector(self, document_id):
        self._create_vector(document_id)

    def _get_vector_if_exists(self, document_id):
        c = self._conn.cursor()
        c.execute(
            '''
            SELECT      term_id, name, value
            FROM        UserVector
            WHERE       user_id = 
                            (
                                SELECT  user_id
                                FROM    UserManagement
                                WHERE   name = :document_id
                            )
            ;
            ''', {'document_id': document_id}
        )
        raise NotImplementedError()
        pass

    def _create_vector(self, document_id):
        pass



