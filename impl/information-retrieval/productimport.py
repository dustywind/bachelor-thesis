#!/usr/bin/python

__author__ = 'dust'

import codecs
import pdb
import sys
import traceback

import irdb
import product


__database_path = '../database'
__database_name = 'test.db'

def main():
    dm = irdb.DatabaseManager(__database_path, __database_name)

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
