
import unittest
import math
import sqlite3

import recommender

test_description_blouse_1 = 'http://i1.ztat.net/large/4E/M2/1E/00/0K/11/4EM21E000-K11@4.jpg Emoi en Plus Bluse - dazzling blue 24,95 € 50 cm 70 cm bei Größe 44 Rundhals 100% Polyester'

test_description_blouse_2 = 'http://i2.ztat.net/large/NA/52/1D/03/NA/11/NA521D03N-A11@3.jpg NAF NAF WENT - Bluse - ecru/noir 38,95 €  55 cm bei Größe S Rundhals 64% Viskose, 22% Baumwolle, 10% Modal, 4% Polyamid'

test_description_trouser_1 = 'http://i1.ztat.net/large/DI/62/2X/00/Q8/58/DI622X00Q-858@1.1.jpg Dickies SLIM STRAIGHT WORK PANT - Chino - schwarz 54,95 € 79 cm bei Größe 32/32 103 cm bei Größe 32/32 verdeckter Zip-Fly Gesäßtaschen normal 65% Polyester, 35% Baumwolle'

test_description_trouser_2 = 'http://i1.ztat.net/large/NI/12/2J/04/5C/00/NI122J045-C00@6.jpg Nike Sportswear VENOM - Trainingshose - dark grey 69,95 € 82 cm bei Größe M 110 cm bei Größe M  Seitentaschen, Gesäßtaschen  100% Baumwolle'


        
class VectorCreatorTestCase(unittest.TestCase):

    def setUp(self):
        global test_description_blouse_1
        global test_description_blouse_2
        self.conn = get_database()
        self.dm = get_database_manager(self.conn)
        self.cm = self.dm.get_product_manager()
        self.cm.add_document(create_blouse(test_description_blouse_1))
        self.cm.add_document(create_blouse(test_description_blouse_2))
        self.pvm = self.dm.get_product_vector_manager()


    def tearDown(self):
        self.conn.close()

    def test_term_frequency_vector_creator(self):
        v1 = self.pvm.get_term_frequency_vector(1)
        v2 = self.pvm.get_term_frequency_vector(2)

        d1 = v1.as_description_dictionary()
        d2 = v2.as_description_dictionary()

        expected_d1 = {
            'Emoi en Plus': 1,
            'Bluse': 1,
            'dazzling blue': 1,
            '2495': 1,
            'Polyester': 1,
            'Rundhals': 1,
            'NAF NAF WENT': 0,
            'ecru': 0,
            'noir': 0,
            '3895': 0,
            'Viskose': 0,
            'Baumwolle': 0,
            'Modal': 0,
            'Polyamid': 0
        }

        expected_d2 = {
            'Emoi en Plus': 0,
            'Bluse': 1,
            'dazzling blue': 0,
            '2495': 0,
            'NAF NAF WENT': 1,
            'Polyester': 0,
            'Rundhals': 1,
            'ecru': 1,
            'noir': 1,
            '3895': 1,
            'Viskose': 1,
            'Baumwolle': 1,
            'Modal': 1,
            'Polyamid': 1
        }

        self.assertEqual(expected_d1, d1, 'expected: %s, got %s' % (expected_d1, d1))
        self.assertEqual(expected_d2, d2, 'expected: %s, got %s' % (expected_d2, d2))
        pass

    def test_document_frequency_vector_creator(self):
        v = self.pvm.get_document_frequency_vector()
        d = v.as_description_dictionary()
        expected_d = {
            'Emoi en Plus': 1,
            'Bluse': 2,
            'dazzling blue': 1,
            '2495': 1,
            'NAF NAF WENT': 1,
            'Polyester': 1,
            'Rundhals': 2,
            'ecru': 1,
            'noir': 1,
            '3895': 1,
            'Viskose': 1,
            'Baumwolle': 1,
            'Modal': 1,
            'Polyamid': 1
        }
        self.assertEqual(expected_d, d, 'expected: %s, got %s' % (expected_d, d))

    def test_inverse_document_frequency_vector_creator(self):
        v = self.pvm.get_inverse_document_frequency_vector(None)
        d = v.as_description_dictionary()

        expected_d = {
            'Emoi en Plus': 0.5,
            'Bluse': 1.0,
            'dazzling blue': 0.5,
            '2495': 0.5,
            'NAF NAF WENT': 0.5,
            'Polyester': 0.5,
            'ecru': 0.5,
            'noir': 0.5,
            '3895': 0.5,
            'Viskose': 0.5,
            'Baumwolle': 0.5,
            'Modal': 0.5,
            'Polyamid': 0.5
        }

    def test_tfidf_vector_creator(self):
        v1 = self.pvm.get_tfidf_vector(1)
        v2 = self.pvm.get_tfidf_vector(2)

        d1 = v1.as_description_dictionary()
        d2 = v2.as_description_dictionary()

        expected_d1 = {
            'Emoi en Plus': 0.5,
            'Bluse': 1,
            'dazzling blue': 0.5,
            '2495': 0.5,
            'NAF NAF WENT': 0.0,
            'Polyester': 0.5,
            'Rundhals': 1.0,
            'ecru': 0.0,
            'noir': 0.0,
            '3895': 0.0,
            'Viskose': 0.0,
            'Baumwolle': 0.0,
            'Modal': 0.0,
            'Polyamid': 0.0
        }

        expected_d2 = {
            'Emoi en Plus': 0.0,
            'Bluse': 1,
            'dazzling blue': 0.0,
            '2495': 0.0,
            'NAF NAF WENT': 0.5,
            'Polyester': 0.0,
            'Rundhals': 1.0,
            'ecru': 0.5,
            'noir': 0.5,
            '3895': 0.5,
            'Viskose': 0.5,
            'Baumwolle': 0.5,
            'Modal': 0.5,
            'Polyamid': 0.5
        }

        self.assertEqual(expected_d1, d1)
        self.assertEqual(expected_d2, d2)
        
class UserVectorManagerTestCase(unittest.TestCase):

    def setUp(self):
        global test_description_blouse_1
        global test_description_blouse_2

        self.conn = get_database()
        self.dm = get_database_manager(self.conn)

        self.document_id_1 = 1
        self.cm = self.dm.get_product_manager()
        self.cm.add_document(create_blouse(test_description_blouse_1))
        self.document_id_2 = 2
        self.cm.add_document(create_blouse(test_description_blouse_2))

        self.cvm = self.dm.get_product_vector_manager()

        self.um = self.dm.get_user_vector_manager()
        pass

    def tearDown(self):
        self.conn.close()

    def test_create_user(self):
        self.um.create_user(1)
        self.um.create_user(2)
        self.um.create_user(4)
        self.um.create_user(7)
        result = self.conn.cursor().execute('SELECT [user_id] FROM [UserManagement];').fetchall()

        expected = [
            (1,), 
            (2,), 
            (4,), 
            (7,), 
        ]

        self.assertEqual(expected, result)
        pass

    def test_has_user_with_id(self):
        id_1 = 1
        id_2 = 2
        self.um.create_user(id_1)

        self.assertTrue(self.um.has_user_with_id(id_1))
        self.assertFalse(self.um.has_user_with_id(id_2))
        pass
        
    def test_get_relevant_documents(self):
        user_id = 1
        self.um.create_user(user_id)

        self.um.set_user_preference(user_id, self.document_id_1, True)

        self.assertEqual(1, len(self.um.get_relevant_document_vector_list(user_id)))
        self.assertEqual(1, len(self.um.get_non_relevant_document_vector_list(user_id)))

        self.um.set_user_preference(user_id, self.document_id_1, False)

        self.assertEqual(0, len(self.um.get_relevant_document_vector_list(user_id)))
        self.assertEqual(2, len(self.um.get_non_relevant_document_vector_list(user_id)))

        self.um.set_user_preference(user_id, self.document_id_1, True)
        self.um.set_user_preference(user_id, self.document_id_2, True)

        self.assertEqual(2, len(self.um.get_relevant_document_vector_list(user_id)))
        self.assertEqual(0, len(self.um.get_non_relevant_document_vector_list(user_id)))
    
        
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

