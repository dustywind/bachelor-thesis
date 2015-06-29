
import sqlite3

class TableCreator(object):
    """abstract class to unify the process of table-creation

    :param sqlite3_connection: an opened instance of a database connection
    :type sqlite3_connection: sqlite3.Connection
    """

    def __init__(self, sqlite3_connection):
        if not isinstance(sqlite3_connection, sqlite3.Connection):
            raise TypeError('Expected sqlite3.Connection as parameter')
        self._conn = sqlite3_connection
        pass

    def init_database(self):
        """Must ve *overwriten* by inheriting classes.

        Should be used to create missing classes
        """
        raise NotImplementedError()
