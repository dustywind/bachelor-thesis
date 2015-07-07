
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
        pass


class VectorArithmeticTest(unittest.TestCase):

    def setUp(self):
        self.vc = recommender.vector.debug.DebugVectorCreator()

        pass

    def tearDown(self):
        pass

    def test_vector_add(self):
        v1 = self.vc.get_vector()
        v2 = self.vc.get_vector()
        expected = self.vc.get_vector()

        v1.add_value(4)
        v1.add_value(4)
        v1.add_value(4)
        v1.add_value(4)
        v1.add_value(4)

        v2.add_value(0.2)
        v2.add_value(0.4)
        v2.add_value(0.9)
        v2.add_value(1.5)
        v2.add_value(4) 

        result_1 = recommender.vector.add(v1, v2)
        result_2 = v1 + v2
        
        expected.add_value(4.2)
        expected.add_value(4.4)
        expected.add_value(4.9)
        expected.add_value(5.5)
        expected.add_value(8)
        
        self.assertEqual(expected.term_id, result_1.term_id)
        self.assertEqual(expected.values, result_1.values)

        self.assertEqual(expected.term_id, result_2.term_id)
        self.assertEqual(expected.values, result_2.values)
        pass

    def test_vector_substract(self):
        v1 = self.vc.get_vector()
        v2 = self.vc.get_vector()
        expected = self.vc.get_vector()

        v1.add_value(4)
        v1.add_value(4)
        v1.add_value(4)
        v1.add_value(4)
        v1.add_value(4)

        v2.add_value(0.2)
        v2.add_value(0.4)
        v2.add_value(0.9)
        v2.add_value(1.5)
        v2.add_value(9) 

        result_1 = recommender.vector.substract(v1, v2)
        result_2 = v1 - v2
        
        expected.add_value(3.8)
        expected.add_value(3.6)
        expected.add_value(3.1)
        expected.add_value(2.5)
        expected.add_value(-5)
        
        self.assertEqual(expected.term_id, result_1.term_id)
        self.assertEqual(expected.values, result_1.values)

        self.assertEqual(expected.term_id, result_2.term_id)
        self.assertEqual(expected.values, result_2.values)
        pass

    def test_vector_scalar_multiplication(self):
        scalar = 3.4
        v1 = self.vc.get_vector()
        expected = self.vc.get_vector()

        v1.add_value(-2)
        v1.add_value(-1)
        v1.add_value(0)
        v1.add_value(1)
        v1.add_value(1.5)

        expected.add_value(-6.8)
        expected.add_value(-3.4)
        expected.add_value(0)
        expected.add_value(3.4)
        expected.add_value(5.1)

        result_1 = recommender.vector.scalar_multiplication(v1, scalar)
        result_2 = v1.scalar_multiplication(scalar)

        self.assertEqual(expected.term_id, result_1.term_id)
        self.assertEqual(expected.values, result_1.values)

        self.assertEqual(expected.term_id, result_2.term_id)
        self.assertEqual(expected.values, result_2.values)

        pass

    def test_vector_euclidean_distance(self):
        v1 = self.vc.get_vector()
        v2 = self.vc.get_vector()
        expected = self.vc.get_vector()

        v1.add_value(4)
        v1.add_value(-1)
        v1.add_value(23)
        v1.add_value(2)
        v1.add_value(0)

        v2.add_value(2)
        v2.add_value(0.4)
        v2.add_value(-0.9)
        v2.add_value(2)
        v2.add_value(9) 

        result = recommender.vector.euclidean_distance(v1, v2)

        t1 = (4 - 2) ** 2
        t2 = (-1 - 0.4) ** 2
        t3 = (23 + 0.9) ** 2
        t4 = (2 - 2) ** 2
        t5 = (0 - 9) ** 2

        expected = math.sqrt( t1 + t2 + t3 + t4 + t5)

        self.assertEqual(expected, result)
    
       
    def test_vector_hamming_distance(self):
        v1 = self.vc.get_vector()
        v2 = self.vc.get_vector()
        expected = self.vc.get_vector()

        v1.add_value(4)
        v1.add_value(-1)
        v1.add_value(23)
        v1.add_value(2)
        v1.add_value(0)

        v2.add_value(2)
        v2.add_value(0.4)
        v2.add_value(-0.9)
        v2.add_value(2)
        v2.add_value(9) 

        result = recommender.vector.hamming_distance(v1, v2)

        expected_value = 4

        self.assertEqual(expected_value, result)
    
        
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

