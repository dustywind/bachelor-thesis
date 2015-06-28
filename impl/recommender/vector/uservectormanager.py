
import sys

from .vectormanager import VectorManager
from .usertablecreator import UserTableCreator
from .user import UserVectorCreator

class UserVectorManager(VectorManager):


    def __init__(self, database_manager):
        super(UserVectorManager, self).__init__(database_manager)
        self._conn = database_manager._conn

        table_creator = UserTableCreator(self._conn)
        table_creator.init_database()

        self._user_vector_creator = UserVectorCreator(self._conn)
        self._product_vector_manager = self._database_manager.get_product_vector_manager()
        pass

    def build_dependencies(self):
        self._database_manager.get_product_vector_manager()
        pass

    def create_user(self, user_id):
        if self.has_user_with_id(user_id):
            raise Exception('user does already exist')
        try:
            self._create_user(user_id)
            empty_vector = self._user_vector_creator.get_empty_vector()
            self._insert_user_vector(user_id, empty_vector)
        except:
            self._conn.rollback()
            raise Exception(sys.exc_info())
        else:
            self._conn.commit()
        pass

    def has_user_with_id(self, user_id):
        c = self._conn.cursor()
        c.execute(
            '''
            SELECT  1
            FROM    UserManagement
            WHERE   user_id = :user_id
            ;
            ''', {'user_id': user_id}
        )
        return c.fetchone() is not None

    def _create_user(self, user_id):
        c = self._conn.cursor()
        c.execute(
            '''
            INSERT INTO UserManagement
            VALUES  (:user_id, :user_id)
            ;
            ''', {'user_id': user_id}
        )
    
    def get_user_vector(self, user_id):
        user_vector = self._user_vector_creator.get_vector(user_id)
        return user_vector

    def _insert_user_vector(self, user_id, user_vector):
        c = self._conn.cursor()
        for (term_id, value) in zip(user_vector.term_id, user_vector.values):
            c.execute(
                '''
                INSERT OR REPLACE INTO
                UserVector  (user_id, term_id, value)
                VALUES      (:user_id, :term_id, :value)
                ;
                ''', {'user_id': user_id, 'term_id': term_id, 'value': value}
            )

    def update_user_vector(self, user_id, user_vector):
        if not self.has_user_with_id(user_id):
            raise Exception('no such user')
        try:
            c = self._conn.cursor()
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
            self._conn.rollback()
            raise Exception(sys.exc_info())
        else:
            self._conn.commit()
        pass


    def get_relevant_document_vector_list(self, user_id):
        """
        :returns: [DocumentVector]
        """
        c = self._conn.cursor()
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
        c = self._conn.cursor()
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
        try:
            if relevant:
                self._mark_as_relevant(user_id, document_id)
            else:
                self._mark_as_non_relevant(user_id, document_id)
        except:
            self._conn.rollback()
            raise Exception(sys.exc_info())
        else:
            self._conn.commit()
        pass
        
    def _mark_as_relevant(self, user_id, document_id):
        c = self._conn.cursor()
        c.execute(
            '''
            INSERT OR IGNORE INTO
            UserPreference  (user_id, document_id)
            VALUES          (:user_id, :document_id)
            ;
            ''', {'user_id': user_id, 'document_id': document_id}
        )
        pass
        
    def _mark_as_non_relevant(self, user_id, document_id):
        c = self._conn.cursor()
        c.execute(
            '''
            DELETE FROM UserPreference
            WHERE       user_id = :user_id
                        AND document_id = :document_id
            ;
            ''', {'user_id': user_id, 'document_id': document_id}
        )
        pass
        





