

import pdb
import sqlite3
import sys

from ..document.documentmanager import DocumentManager
from .producttablecreator import ProductTableCreator
from .product import Product

class ProductManager(DocumentManager):

    def __init__(self, database_manager):
        super(ProductManager, self).__init__(database_manager)

        table_creator = ProductTableCreator(self._db_connection_str)
        table_creator.init_database()

        self._document_manager = self._database_manager.get_document_manager()
        self._term_manager = self._database_manager.get_term_manager()
        pass

    def build_dependencies(self):
        """has no dependencies
        self._database_manager.get_document_manager()
        """
        self._database_manager.get_term_manager()
        self._database_manager.get_document_manager()
        pass

    def add_document(self, product):

        #pdb.set_trace()

        with self._get_db_connection() as conn:
            try:
                document_id = self._document_manager.get_new_document_id()

                cursor = conn.cursor()
                self._insert_product(cursor, document_id, product)

                term_tuple_list = []

                for term_name in product.terms:
                    term_tuple_list.append((term_name, product.terms[term_name]))
                self._term_manager.temp_conn = conn
                self._term_manager.add_terms(document_id, term_tuple_list)
                self._term_manager.temp_conn = None
            except Exception:
                conn.rollback()
                raise Exception(sys.exc_info())
            else:
                conn.commit()

    def get_product(self, document_id):
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            image_name = self._get_product_image(cursor, document_id)
        attr_dict = self._get_terms()

        p = Product()
        p.document_id = document_id
        p.image_name = image_name
        p.terms = attr_dict
        return p

    def _get_product_image(self, c, document_id):
        c.execute(
            '''
            SELECT
                image_name
            FROM
                Product
            WHERE
                document_id = :document_id
            ;
            ''', {'document_id': document_id}
        )
        pass

    def _get_terms(self, document_id):
        terms = self._term_manager.get_terms(document_id)
        return terms

    def _insert_product(self, c, document_id, product):
        c.execute(
            '''
            INSERT OR IGNORE INTO Product
            VALUES (:document_id, :img_name)
            ;
            ''', {'document_id': document_id, 'img_name': product.image_name}
        )
        pass




