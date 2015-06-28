
import sqlite3

class TableCreator(object):
    """information retrieval database connector
    """

    def __init__(self, sqlite3_connection):
        """
        """
        if not isinstance(sqlite3_connection, sqlite3.Connection):
            raise TypeError('Expected sqlite3.Connection as parameter')
        self._conn = sqlite3_connection
        pass

    def init_database(self):
        raise NotImplementedError()
