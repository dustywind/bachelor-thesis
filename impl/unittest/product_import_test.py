
import unittest
import math
import sqlite3

import recommender

class ProductImportTestCase(unittest.TestCase):

    def setUp(self):
        self.conn = get_database()
        self.dm = get_database_manager(self.conn)
        self.pm = self.dm.get_product_manager()
        self.tm = self.dm.get_term_manager()

    def tearDown(self):
        pass

    def test_import(self):
        p1 = recommender.product.Product()
        p1.image_name = 'image_01'
        p1.terms = {
            'a': 1,
            'b': 2,
            'x': 1
        }
        p2 = recommender.product.Product()
        p2.image_name = 'image_02'
        p2.terms = {
            'a': 1,
            'b': 1,
            'y': 5
        }
        p3 = recommender.product.Product()
        p3.image_name = 'image_03'
        p3.terms = {
            'a': 1,
            'b': 1,
            'y': 5
        }
        p4 = recommender.product.Product()
        p4.image_name = 'image_04'
        p4.terms = {
            'k': 1,
            'l': 3
        }

        self.pm.add_document(p1)
        self.pm.add_document(p2)
        self.pm.add_document(p3)
        self.pm.add_document(p4)


        result = self.tm.get_sum_of_terms()
        expected = {
            'a': 3,
            'b': 4,
            'k': 1,
            'l': 3,
            'x': 1,
            'y': 10
        }
        
        self.assertEqual(expected, result)
        pass

        
def get_database_manager(conn):
    return recommender.DatabaseManager(conn)

def get_database():
    tmp_database = "unittest/test.sqlite3"
    try:
        import os
        os.remove(tmp_database)
    except:
        pass
    return tmp_database


create_blouse_count = 0
def create_blouse(description):
    return recommender.product.ProductCreator.create_lady_blouse_from_description(description)

if __name__ == '__main__':
    print('hi')
    unittest.main()

