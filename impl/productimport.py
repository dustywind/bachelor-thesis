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

    import_lady_blouses(dm)
    import_gentleman_trousers(dm)

    dm.get_user_vector_manager()
    pass

def import_lady_blouses(dm):
    lady_blouses = codecs.open('./product_data/DamenBlusen.txt', 'r', 'utf-8')
    lady_blouses.readline() # skip first line

    product_creator = recommender.product.ProductCreator
    product_manager = dm.get_product_manager()

    for line in lady_blouses:
        try:
            product = product_creator.create_lady_blouse_from_description(line)
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


def import_gentleman_trousers(dm):
    gentleman_trousers = codecs.open('./product_data/HerrenHosen.txt', 'r', 'utf-8')
    gentleman_trousers.readline() # skip first line

    product_creator = recommender.product.ProductCreator
    product_manager = dm.get_product_manager()

    for line in gentleman_trousers:
        try:
            product = product_creator.create_gentleman_trouser_from_description(line)
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


if __name__ == '__main__':
    import_products()
    pass


