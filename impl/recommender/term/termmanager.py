
from ..dependency import Dependency
from ..document import DocumentManager
from .termtablecreator import TermTableCreator

class TermManager(DocumentManager):

    def __init__(self, database_manager):
        super(TermManager, self).__init__(database_manager)
        self._conn = self._database_manager._conn
        
        table_creator = TermTableCreator(self._conn)
        table_creator.init_database()
        pass

    def build_dependencies(self):
        self._database_manager.get_document_manager()
        pass

    def add_terms(self, document_id, term_tuple_list):
        for term_name, count in term_tuple_list:
            if not self.has_term(term_name):
                self._create_term(term_name)
            term_id = self.get_term_id(term_name)
            self._assign_term_to_document(term_id, document_id, count)
        pass

    def _create_term(self, term_name):
        c = self._conn.cursor()
        c.execute(
            '''
            INSERT INTO Term
            (term_id, name)
            VALUES (null, :term_name)
            ''', {'term_name': term_name}
        )
        pass

    def get_term_id(self, term_name):
        c = self._conn.cursor()
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
        pass

    def _assign_term_to_document(self, term_id, document_id, count):
        c = self._conn.cursor()
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

    def get_sum_of_terms(self):
        c = self._conn.cursor()
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
        c = self._conn.cursor()
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














