
import sqlite3
import sys

from ..abstractvector import VectorCreator
from ..empty import EmptyVectorCreator
from .uservector import UserVector

class UserVectorCreator(VectorCreator):
    
    def __init__(self, sqlite3_connection):
       super(UserVectorCreator, self).__init__(sqlite3_connection)
       self._empty_creator = EmptyVectorCreator(self._conn)
       pass

    def get_vector(self, document_id):
        #vector = self._get_or_create_vector(document_id)
        vector = self._get_vector(document_id)
        return vector

    def get_empty_vector(self):
        empty = self._empty_creator.get_vector()
        return empty

    def has_vector(self, user_id):
        c = self._conn.cursor()
        c.execute(
            '''
            SELECT      *
            FROM        UserVector
            WHERE       user_id = :user_id
            ''', {'user_id': user_id}
        )
        return c.fetchone() is not None

    def _get_vector(self, user_id):
        c = self._conn.cursor()
        c.execute(
            '''
            SELECT      t.term_id
                        , t.name
                        , uv.value
            FROM        Term AS t
                        JOIN UserVector AS uv
                        ON t.term_id = uv.term_id
            WHERE       uv.user_id = :user_id
            ORDER BY    t.term_id
            ;
            ''', {'user_id': user_id}
        )
        document_vector = UserVector()
        for row in c.fetchall():
            triple = (row[0], row[1], row[2])
            document_vector.add_to_vector(triple)
        return document_vector

