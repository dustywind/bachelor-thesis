
import os
import sqlite3
import sys

from clothingtablecreator import ClothingTableCreator
from clothingmanager import ClothingManager

import vector

class DatabaseManager(object):
    
    def __init__(self, db_path, db_name):
        self._db_full_path = os.path.join(db_path, db_name)

        self.__connect_to_db()

        tc = ClothingTableCreator(self.__conn)
        tc.create_tables()
        pass

    def __del__(self):
        self.close()

    def __connect_to_db(self):
        """
        Opens a connection to the given database
        """
        try:
            self.__conn = sqlite3.connect(self._db_full_path)
            c = self.__conn.cursor()
            c.execute('PRAGMA foreign_keys=ON')
        except Exception:
            self.__conn.rollback()
            raise Exception(sys.exc_info())
        else:
            self.__conn.commit()

    def close(self):
        """
        Closes the connection to the database
        """
        if self.__conn is not None:
            self.__conn.close()

    def create_clothingmanager(self):
        return ClothingManager(self.__conn)

    def create_vectormanager(self):
        return vector.ClothingVectorManager(self.__conn)






