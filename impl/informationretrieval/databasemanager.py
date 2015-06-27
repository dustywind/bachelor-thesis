
import os
import sqlite3
import sys
import pdb

from informationretrieval.vector import ProductVectorManager
from informationretrieval.vector import UserVectorManager
from informationretrieval.product import ProductManager
from informationretrieval.term import TermManager
from informationretrieval.document import DocumentManager

class DatabaseManager(object):
    
    def __init__(self, sqlite3_connection):
        if not isinstance(sqlite3_connection, sqlite3.Connection):
            raise TypeError('expects a sqlite3-connection as parameter')
        self._conn = sqlite3_connection

        self._product_vector_manager = None
        self._user_vector_manager = None
        self._document_manager = None
        self._term_manager = None
        self._product_manager = None

        self.enforce_foreign_keys()
        pass

    def __del__(self):
        self.close()

    def enforce_foreign_keys(self):
        """Enforces foreign key constraints on tables
        """
        try:
            c = self._conn.cursor()
            c.execute('PRAGMA foreign_keys=ON')
        except Exception:
            self._conn.rollback()
            raise Exception(sys.exc_info())
        else:
            self._conn.commit()

    def close(self):
        """
        Closes the connection to the database
        """
        if self._conn is not None:
            self._conn.close()

    def get_product_vector_manager(self):
        #pdb.set_trace()
        if not self._product_vector_manager:
            self._product_vector_manager = ProductVectorManager(self)
        return self._product_vector_manager

    def get_user_vector_manager(self):
        if not self._user_vector_manager:
            self._user_vector_manager = UserVectorManager(self)
        return self._user_vector_manager

    def get_product_manager(self):
        if not self._product_manager:
            self._product_manager = ProductManager(self)
        return self._product_manager

    def get_term_manager(self):
        if not self._term_manager:
            self._term_manager = TermManager(self)
        return self._term_manager

    def get_document_manager(self):
        if not self._document_manager:
            self._document_manager = DocumentManager(self)
        return self._document_manager


