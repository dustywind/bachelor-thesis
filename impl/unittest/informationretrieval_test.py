
import unittest
import sqlite3

import informationretrieval

test_description_1 = 'http://i1.ztat.net/large/4E/M2/1E/00/0K/11/4EM21E000-K11@4.jpg Emoi en Plus Bluse - dazzling blue 24,95 € 50 cm 70 cm bei Größe 44 Rundhals 100% Polyester'

test_description_2 = 'http://i2.ztat.net/large/NA/52/1D/03/NA/11/NA521D03N-A11@3.jpg NAF NAF WENT - Bluse - ecru/noir 38,95 €  55 cm bei Größe S Rundhals 64% Viskose, 22% Baumwolle, 10% Modal, 4% Polyamid'

"""
class ClothingImportTestCase(unittest.TestCase):

    def setUp(self):
        self.conn = get_database()
        self.dm = get_database_manager(self.conn)
        self.cm = self.dm.get_product_manager()

    def tearDown(self):
        self.conn.close()

    def test_import_1(self):
        global test_description_1
        global test_description_2
        c = create_product(test_description_1)
        self.cm.add_document(c)
        c = create_product(test_description_2)
        self.cm.add_document(c)

        product_count = len(self.conn.cursor().execute('select * from Product;').fetchall())
        expected_materials = ['Polyester', 'Viskose', 'Baumwolle', 'Modal', 'Polyamid']
        materials = [ val for (index, val) in self.conn.cursor().execute('select * from Material;').fetchall() ]
        expected_colours = ['dazzling blue', 'ecru', 'noir']
        colours = [ val for (index, val) in self.conn.cursor().execute('select * from Colour;').fetchall() ]

        self.assertEqual(2, product_count, 'actual count is %d, shoud be 1'% product_count)
        self.assertEqual(expected_materials, materials, 'expected %s, got %s' % (expected_materials, materials))
        self.assertEqual(expected_colours, colours, 'expected %s, got %s' % (expected_colours, colours))
"""


class VectorCreatorTestCase(unittest.TestCase):

    def setUp(self):
        global test_description_1
        global test_description_2
        self.conn = get_database()
        self.dm = get_database_manager(self.conn)
        self.cm = self.dm.get_product_manager()
        self.cm.add_document(create_product(test_description_1))
        self.cm.add_document(create_product(test_description_2))
        self.vm = self.dm.get_product_vector_manager()


    def tearDown(self):
        self.conn.close()

    def test_term_frequency_vector_creator(self):
        v1 = self.vm.get_term_frequency_vector(1)
        v2 = self.vm.get_term_frequency_vector(2)

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
        v = self.vm.get_document_frequency_vector()
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
        v = self.vm.get_inverse_document_frequency_vector(None)
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
        v1 = self.vm.get_tfidf_vector(1)
        v2 = self.vm.get_tfidf_vector(2)

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
        global test_description_1
        global test_description_2

        self.conn = get_database()
        self.dm = get_database_manager(self.conn)

        self.document_id_1 = 1
        self.cm = self.dm.get_product_manager()
        self.cm.add_document(create_product(test_description_1))
        self.document_id_2 = 2
        self.cm.add_document(create_product(test_description_2))

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
        self.vc = informationretrieval.vector.debug.DebugVectorCreator()

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

        result_1 = informationretrieval.vector.add(v1, v2)
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

        result_1 = informationretrieval.vector.substract(v1, v2)
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

        result_1 = informationretrieval.vector.scalar_multiplication(v1, scalar)
        result_2 = v1.scalar_multiplication(scalar)

        self.assertEqual(expected.term_id, result_1.term_id)
        self.assertEqual(expected.values, result_1.values)

        self.assertEqual(expected.term_id, result_2.term_id)
        self.assertEqual(expected.values, result_2.values)

        pass
    
        
def get_database_manager(conn):
    return informationretrieval.DatabaseManager(conn)


def get_database():
    conn = sqlite3.connect(':memory:')
    return conn


create_product_count = 0
def create_product(description):
    return informationretrieval.product.ProductCreator.create_from_description(description)

if __name__ == '__main__':
    print('hi')
    unittest.main()

