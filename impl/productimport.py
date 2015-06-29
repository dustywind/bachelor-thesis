#!/usr/bin/env python3


"""
Module productimport description
"""

import codecs
import pdb
import sys
import sqlite3
import traceback

import recommender


def import_products():
    database_config = './database/recommender.sqlite3'

    sqlite3_connection = sqlite3.connect(database_config)

    dm = recommender.DatabaseManager(sqlite3_connection)

    f = codecs.open('./DamenBlusen.txt', 'r', 'utf-8')
    f.readline() # skip first line

    product_creator = recommender.product.ProductCreator
    product_manager = dm.get_product_manager()

    for line in f:
        try:
            product = product_creator.create_from_description(line)
            product_manager.add_document(product)
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

    #vectormanager = dm.get_clothing_vector_manager()
    dm.get_user_vector_manager()
    pass

if __name__ == '__main__':
    import_products()
    pass


