
import sys

from ..dependency import Dependency
from ..document import DocumentManager
from .termtablecreator import TermTableCreator

class TermManager(DocumentManager):

    def __init__(self, database_manager):
        super(TermManager, self).__init__(database_manager)
        
        table_creator = TermTableCreator(self._db_connection_str)
        table_creator.init_database()
        pass

    def build_dependencies(self):
        self._database_manager.get_document_manager()
        pass

    def add_terms(self, document_id, term_tuple_list):
        with self._get_db_connection() as conn:
            try:
                cursor = conn.cursor()
                self._add_terms(cursor, document_id, term_tuple_list)
            except:
                conn.rollback()
                raise Exception(sys.exc_info())
            else:
                conn.commit()
        pass

    def _add_terms(self, cursor, document_id, term_tuple_list):
        for term_name, count in term_tuple_list:
            if not self._has_term(cursor, term_name):
                self._create_term(cursor, term_name)
            term_id = self._get_term_id(cursor, term_name)
            self._assign_term_to_document(cursor, term_id, document_id, count)
        pass

    def _create_term(self, c, term_name):
        c.execute(
            '''
            INSERT INTO Term
            (term_id, name)
            VALUES (null, :term_name)
            ''', {'term_name': term_name}
        )
        pass

    def get_term_id(self, term_name):
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            return self._get_term_id(cursor, term_name)
            pass

    def _get_term_id(self, c, term_name):
        c.execute(
            '''
            SELECT
                term_id
            FROM
                Term
            WHERE
                name = :term_name
            ;
            ''', {'term_name': term_name}
        )
        result = c.fetchone()
        return None if result is None else result[0]

    def _assign_term_to_document(self, c, term_id, document_id, count):
        c.execute(
            '''
            INSERT OR REPLACE INTO TermDocumentAssigner
            VALUES (:term_id, :document_id, :count)
            ;
            ''', {
                'term_id': term_id,
                'document_id': document_id,
                'count': count
            }
        )
        pass


    def has_term(self, term_name):
        return self.get_term_id(term_name) is not None

    def _has_term(self, c, term_name):
        return self._get_term_id(c, term_name) is not None

    def get_sum_of_terms(self):
        with self._get_db_connection() as conn:
            c = conn.cursor()
            return self._get_sum_of_terms(c)
            
    def _get_sum_of_terms(self, c):
        c.execute(
            ''' 
            SELECT
                t.name
                ,SUM(a.count )
            FROM
                Term as t
                JOIN TermDocumentAssigner AS a ON t.term_id = a.term_id
            GROUP BY
                t.term_id
            ORDER BY
                t.term_id
            ;
            '''
            )
        terms = {}
        for term_name, count in c.fetchall():
            terms[term_name] = count
            pass
        return terms

    def get_terms(self, document_id):
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            self._get_terms(cursor, document_id)
        
    def _get_terms(self, c, document_id):
        c.execute(
            '''
            SELECT
                t.name
                , a.count
            FROM
                Term AS t
                JOIN TermDocumentAssigner AS a ON t.term_id = a.term_id
            WHERE
                a.document_id = :document_id
            ORDER BY
                t.term_id
            ;
            ''', {'document_id': document_id}
        )

        term_freq_dict = {}
        for (term_name, freq) in c.fetchall():
            term_freq_dict[term_name] = freq
        return term_freq_dict


