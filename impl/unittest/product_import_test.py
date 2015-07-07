
import unittest
import math
import sqlite3

import recommender

test_description_blouse_1 = 'http://i1.ztat.net/large/4E/M2/1E/00/0K/11/4EM21E000-K11@4.jpg Emoi en Plus Bluse - dazzling blue 24,95 € 50 cm 70 cm bei Größe 44 Rundhals 100% Polyester'

test_description_blouse_2 = 'http://i2.ztat.net/large/NA/52/1D/03/NA/11/NA521D03N-A11@3.jpg NAF NAF WENT - Bluse - ecru/noir 38,95 €  55 cm bei Größe S Rundhals 64% Viskose, 22% Baumwolle, 10% Modal, 4% Polyamid'

test_description_trouser_1 = 'http://i1.ztat.net/large/DI/62/2X/00/Q8/58/DI622X00Q-858@1.1.jpg Dickies SLIM STRAIGHT WORK PANT - Chino - schwarz 54,95 € 79 cm bei Größe 32/32 103 cm bei Größe 32/32 verdeckter Zip-Fly Gesäßtaschen normal 65% Polyester, 35% Baumwolle'

test_description_trouser_2 = 'http://i1.ztat.net/large/NI/12/2J/04/5C/00/NI122J045-C00@6.jpg Nike Sportswear VENOM - Trainingshose - dark grey 69,95 € 82 cm bei Größe M 110 cm bei Größe M  Seitentaschen, Gesäßtaschen  100% Baumwolle'


class ProductImportTestCase(unittest.TestCase):

    def setUp(self):
        self.conn = get_database()
        self.dm = get_database_manager(self.conn)
        self.pm = self.dm.get_product_manager()
        self.tm = self.dm.get_term_manager()

    def tearDown(self):
        self.conn.close()

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
    conn = sqlite3.connect(':memory:')
    return conn


create_blouse_count = 0
def create_blouse(description):
    return recommender.product.ProductCreator.create_lady_blouse_from_description(description)

if __name__ == '__main__':
    print('hi')
    unittest.main()

