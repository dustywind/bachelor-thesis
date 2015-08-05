
import sys

from .vectormanager import VectorManager
from .usertablecreator import UserTableCreator
from .user import UserVectorCreator

class UserVectorManager(VectorManager):


    def __init__(self, database_manager):
        super(UserVectorManager, self).__init__(database_manager)

        table_creator = UserTableCreator(self._db_connection_str)
        table_creator.init_database()

        self._user_vector_creator = UserVectorCreator(self._db_connection_str)
        self._product_vector_manager = database_manager.get_product_vector_manager()
        pass

    def build_dependencies(self):
        self._database_manager.get_product_vector_manager()
        pass

    def create_user(self, user_name):
        if self.has_user_with_name(user_name):
            raise Exception('user does already exist')
        with self._get_db_connection() as conn:
            try:
                cursor = conn.cursor()

                self._create_user(cursor, user_name)
                user_id = self._get_user_id_for_name(cursor, user_name)
                empty_vector = self._user_vector_creator.get_empty_vector()
                self._insert_user_vector(cursor, user_id, empty_vector)
            except:
                conn.rollback()
                raise Exception(sys.exc_info())
            else:
                conn.commit()
            pass
        pass

    def has_user_with_id(self, user_id):
        with self._get_db_connection() as conn:
            c = conn.cursor()
            c.execute(
                '''
                SELECT  1
                FROM    User
                WHERE   user_id = :user_id
                ;
                ''', {'user_id': user_id}
            )
            return c.fetchone() is not None
    
    def has_user_with_name(self, user_name):
        with self._get_db_connection() as conn:
            c = conn.cursor()
            c.execute(
                '''
                SELECT  1
                FROM    User
                WHERE   name = :user_name
                ;
                ''', {'user_name': user_name}
            )
            return c.fetchone() is not None
        pass

    def get_all_users_by_name(self):
        with self._get_db_connection() as conn:
            c = conn.cursor()
            c.execute(
                '''
                SELECT
                    name
                FROM
                    User
                ORDER BY
                    user_id
                ;
                '''
            )
            return [ user_name for (user_name, ) in c.fetchall()]
        pass

    def get_user_id_for_name(self, user_name):
        with self._get_db_connection() as conn:
            c = conn.cursor()
            return self._get_user_id_for_name(c, user_name)

    def _get_user_id_for_name(self, cursor, user_name):
        cursor.execute(
            '''
            SELECT
                user_id
            FROM
                User
            WHERE
                name = :user_name
            ;
            ''', {'user_id': None, 'user_name': user_name}
        )
        result = cursor.fetchone()
        return None if result is None else result[0]

    def _create_user(self, c, user_name):
        c.execute(
            '''
            INSERT INTO
                User
            VALUES
                (:user_id, :user_name)
            ;
            ''', {'user_id': None, 'user_name': user_name}
        )
        
    def get_user_vector_for_id(self, user_id):
        user_vector = self._user_vector_creator.get_vector(user_id)
        return user_vector

    def get_user_vector_for_name(self, user_name):
        user_id = self.get_user_id_for_name(user_name)
        return self.get_user_vector_for_id(user_id)

    def _insert_user_vector(self, c, user_id, user_vector):
        for (term_id, value) in zip(user_vector.term_id, user_vector.values):
            c.execute(
                '''
                INSERT OR REPLACE INTO
                    UserVector  (user_id, term_id, value)
                VALUES
                    (:user_id, :term_id, :value)
                ;
                ''', {'user_id': user_id, 'term_id': term_id, 'value': value}
            )

    def update_user_vector(self, user_id, user_vector):
        if not self.has_user_with_id(user_id):
            raise Exception('no such user')
        with self._get_db_connection() as conn:
            try:
                c = conn.cursor()
                for term_id, value in zip(user_vector.term_id, user_vector.values):
                    c.execute(
                        '''
                        UPDATE  UserVector
                        SET     value = :value
                        WHERE   user_id = :user_id
                                AND term_id = :term_id
                        ;
                        ''', {'user_id': user_id, 'term_id': term_id, 'value': value}
                    )
                    pass
            except Exception:
                conn.rollback()
                raise Exception(sys.exc_info())
            else:
                conn.commit()
            pass
        pass


    def get_relevant_document_vector_list(self, user_id):
        """
        :returns: [DocumentVector]
        """
        with self._get_db_connection() as conn:
            c = conn.cursor()
            c.execute(
                '''
                SELECT  document_id
                FROM    UserPreference
                WHERE   user_id = :user_id
                ;
                ''', {'user_id': user_id}
            )
            relevant_docs = [ doc_id for (doc_id,) in c.fetchall() ]
            return self._document_id_list_to_vector_list(relevant_docs)

    def get_non_relevant_document_vector_list(self, user_id):
        """
        """
        with self._get_db_connection() as conn:
            c = conn.cursor()
            c.execute(
                '''
                SELECT
                    p.document_id
                FROM
                    Product AS p
                    LEFT OUTER JOIN
                    (
                        SELECT
                            document_id
                        FROM
                            UserPreference
                        WHERE
                            user_id = :user_id
                    ) AS t
                    ON p.document_id = t.document_id
                WHERE
                    t.document_id IS NULL
                ORDER BY
                    p.document_id
                ''', {'user_id': user_id}
            )
            unrelevant_docs = [doc_id for (doc_id,) in c.fetchall()]
            return self._document_id_list_to_vector_list(unrelevant_docs)

    def _document_id_list_to_vector_list(self, document_id_list):
        cvm = self._product_vector_manager
        l = [cvm.get_vector_for_document_id(d) for d in document_id_list]
        return l

    def set_user_preference(self, user_id, document_id, relevant=True):
        with self._get_db_connection() as conn:
            try:
                cursor = conn.cursor()
                if relevant:
                    self._mark_as_relevant(cursor, user_id, document_id)
                else:
                    self._mark_as_non_relevant(cursor, user_id, document_id)
            except:
                conn.rollback()
                raise Exception(sys.exc_info())
            else:
                conn.commit()
            pass
        
    def _mark_as_relevant(self, c, user_id, document_id):
        c.execute(
            '''
            INSERT OR IGNORE INTO
            UserPreference  (user_id, document_id)
            VALUES          (:user_id, :document_id)
            ;
            ''', {'user_id': user_id, 'document_id': document_id}
        )
        pass
        
    def _mark_as_non_relevant(self, c, user_id, document_id):
        c.execute(
            '''
            DELETE FROM UserPreference
            WHERE       user_id = :user_id
                        AND document_id = :document_id
            ;
            ''', {'user_id': user_id, 'document_id': document_id}
        )
        pass
        



