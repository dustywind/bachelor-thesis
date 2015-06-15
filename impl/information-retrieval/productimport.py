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
    _database_path = '../database'
    _database_name = 'test.db'

    dm = irdb.DatabaseManager(_database_path, _database_name)

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
            print(sys.exc_info())
            print(line)
            pass
        except Exception:
            print(sys.exc_info())
            print(line)
            pass
        pass

    vectormanager = dm.create_vectormanager()
    pass

if __name__ == '__main__':
    main()
