import sqlite3
import sys

from ..abstractvector import VectorCreator
from ..empty import EmptyVectorCreator
from .uservector import UserVector

class UserVectorCreator(VectorCreator):
    
    def __init__(self, db_connection_str):
       super(UserVectorCreator, self).__init__(db_connection_str)
       self._empty_creator = EmptyVectorCreator(db_connection_str)
       pass

    def get_vector(self, document_id):
        #vector = self._get_or_create_vector(document_id)
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            vector = None
            vector = self._get_vector(cursor, document_id)
            return vector

    def get_empty_vector(self):
        empty = self._empty_creator.get_vector()
        return empty

    def has_vector(self, user_id):
        with self._get_db_connection() as conn:
            c = conn.cursor()
            c.execute(
                '''
                SELECT      *
                FROM        UserVector
                WHERE       user_id = :user_id
                ''', {'user_id': user_id}
            )
            return c.fetchone() is not None

    def _get_vector(self, c, user_id):
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

