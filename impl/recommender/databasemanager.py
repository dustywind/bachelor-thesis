
import os
import sqlite3
import sys
import pdb

from recommender.vector import ProductVectorManager
from recommender.vector import UserVectorManager
from recommender.product import ProductManager
from recommender.term import TermManager
from recommender.document import DocumentManager

from recommender.dbconnection import DbConnection

class DatabaseManager(object):
    """The central class in the whole library.
    This class provides the caller with 
        - :class:`recommender.product..ProductManager`
        - :class:`recommender.document.DocumentManager`
        - :class:`recommender.term.TermManager`
        - :class:`recommender.vector.ProductVectorManager`
        - :class:`recommender.vector.UserVectorManager`

    :param sqlite3_connection: a open connection to a database on which the operations shall beperformed 
    :type sqlite3_connection: sqlite3.Connection
    :raises: TypeError, if the argument is not a valid sqlite3.Connection instance
    """
    
    def __init__(self, db_connection_str):
        self._db_connection_str = db_connection_str

        self.enforce_foreign_keys()

        self._product_vector_manager = None
        self._user_vector_manager = None
        self._document_manager = None
        self._term_manager = None
        self._product_manager = None
        pass

    def _get_db_connection(self):
        return DbConnection(self._db_connection_str)

    def get_db_connection_str(self):
        return self._db_connection_str

    def enforce_foreign_keys(self):
        """Enforces foreign key constraints on tables of the database
        """
        with self._get_db_connection() as conn:
            try:
                c = conn.cursor()
                c.execute('PRAGMA foreign_keys=ON')
            except Exception:
                conn.rollback()
                raise Exception(sys.exc_info())
            else:
                conn.commit()

    def get_product_vector_manager(self):
        """Gets an instance of :class:`recommender.vector.ProductVectorManager`

        :returns: :class:`recommender.vector.ProductVectorManager`
        """
        if not self._product_vector_manager:
            self._product_vector_manager = ProductVectorManager(self)
        return self._product_vector_manager

    def get_user_vector_manager(self):
        """Gets an instance of :class:`recommender.vector.ProductVectorManager`

        :returns: :class:`recommender.vector.ProductVectorManager`
        """
        if not self._user_vector_manager:
            self._user_vector_manager = UserVectorManager(self)
        return self._user_vector_manager

    def get_product_manager(self):
        """Gets an instance of :class:`recommender.vector.ProductManager`

        :returns: :class:`recommender.product.ProductManager`
        """
        if not self._product_manager:
            self._product_manager = ProductManager(self)
        return self._product_manager

    def get_term_manager(self):
        """Gets an instance of :class:`recommender.term.TermManager`

        :returns: :class:`recommender.term.TermManager`
        """
        if not self._term_manager:
            self._term_manager = TermManager(self)
        return self._term_manager

    def get_document_manager(self):
        """Gets an instance of :class:`recommender.document.DocumentManager`

        :returns: :class:`recommender.document.DocumentManager`
        """
        if not self._document_manager:
            self._document_manager = DocumentManager(self)
        return self._document_manager


