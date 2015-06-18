"""
Module productimport description
"""


import codecs
import pdb
import sys
import traceback

import irdb
import product


def main():
    database_path = '../database'
    database_name = 'rocchio.sqlite3'

    dm = irdb.DatabaseManager(database_path, database_name)

    f = codecs.open('./DamenBlusen.txt', 'r', 'utf-8')
    f.readline() # skip first line

    clothingmanager = dm.create_clothingmanager()

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

    vectormanager = dm.create_vectormanager()
    pass

if __name__ == '__main__':
    main()
