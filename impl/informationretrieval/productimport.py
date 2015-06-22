"""
Module productimport description
"""

import codecs
import pdb
import sys
import sqlite3
import traceback

from . import irdb
from . import product
from informationretrieval import DatabaseManager


def import_clothing():
    database_config = './database/test.sqlite3'

    sqlite3_connection = sqlite3.connect(database_config)

    dm = DatabaseManager(sqlite3_connection)

    f = codecs.open('./informationretrieval/DamenBlusen.txt', 'r', 'utf-8')
    f.readline() # skip first line

    clothingmanager = dm.get_clothing_manager()

    for line in f:
        try:
            clothing = product.ProductCreator.create_clothing(line)
            clothingmanager.add_document(clothing)
        except UnicodeEncodeError:
            print(sys.exc_info())
            print(line)
            pass
        except ValueError:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print(exc_type)
            print(exc_value)
            print(line)
            pass
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print(exc_type)
            print(exc_value)
            print(exc_traceback)
            pass
        pass

    vectormanager = dm.get_clothing_vector_manager()
    pass

