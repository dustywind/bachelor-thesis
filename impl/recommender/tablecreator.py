
import sqlite3

from . import DbConnection

class TableCreator(object):
    """abstract class to unify the process of table-creation

    :param sqlite3_connection: an opened instance of a database connection
    :type sqlite3_connection: sqlite3.Connection
    """

    def __init__(self, db_connection_str):
        self._db_connection_str = db_connection_str
        pass

    def _get_db_connection(self):
        return DbConnection(self._db_connection_str)

    def init_database(self):
        """Must ve *overwriten* by inheriting classes.

        Should be used to create missing classes
        """
        raise NotImplementedError()
