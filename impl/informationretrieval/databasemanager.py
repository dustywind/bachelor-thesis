
import os
import sqlite3
import sys
import pdb

from informationretrieval.irdb import ClothingManager
from informationretrieval.vector import ClothingVectorManager
from informationretrieval.vector import UserVectorManager

class DatabaseManager(object):
    
    def __init__(self, sqlite3_connection):
        if not isinstance(sqlite3_connection, sqlite3.Connection):
            raise TypeError('expects a sqlite3-connection as parameter')
        self._conn = sqlite3_connection

        self._clothing_manager = None
        self._clothing_vector_manager = None
        self._user_vector_manager = None

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

    def get_clothing_manager(self):
        #pdb.set_trace()
        if not self._clothing_manager:
            self._clothing_manager = ClothingManager(self)
        return self._clothing_manager

    def get_clothing_vector_manager(self):
        #pdb.set_trace()
        if not self._clothing_vector_manager:
            self._clothing_vector_manager = ClothingVectorManager(self)
        return self._clothing_vector_manager

    def get_user_vector_manager(self):
        if not self._user_vector_manager:
            self._user_vector_manager = UserVectorManager(self)
        return self._user_vector_manager


