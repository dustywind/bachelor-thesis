
import sqlite3
import sys
import pdb

from .. import TableCreator

class VectorTableCreator(TableCreator):
    """some comment"""

    def __init__(self, sqlite3_connection):
        super(VectorTableCreator, self).__init__(sqlite3_connection)

    def init_database(self):
        # there used to be some code.
        # but meanwhile it got outsourced to informationretrieval.term
        pass

