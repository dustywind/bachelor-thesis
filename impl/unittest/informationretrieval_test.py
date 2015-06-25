
import unittest
import sqlite3

import informationretrieval

test_description_1 = 'http://i1.ztat.net/large/4E/M2/1E/00/0K/11/4EM21E000-K11@4.jpg Emoi en Plus Bluse - dazzling blue 24,95 € 50 cm 70 cm bei Größe 44 Rundhals 100% Polyester'

test_description_2 = 'http://i2.ztat.net/large/NA/52/1D/03/NA/11/NA521D03N-A11@3.jpg NAF NAF WENT - Bluse - ecru/noir 38,95 €  55 cm bei Größe S Rundhals 64% Viskose, 22% Baumwolle, 10% Modal, 4% Polyamid'

class ClothingImportTestCase(unittest.TestCase):

    def setUp(self):
        self.conn = get_database()
        self.dm = get_database_manager(self.conn)
        self.cm = self.dm.get_clothing_manager()

    def tearDown(self):
        self.conn.close()

    def test_import_1(self):
        global test_description_1
        global test_description_2
        c = create_clothing(test_description_1)
        self.cm.add_document(c)
        c = create_clothing(test_description_2)
        self.cm.add_document(c)

        clothing_count = len(self.conn.cursor().execute('select * from Clothing;').fetchall())
        expected_materials = ['Polyester', 'Viskose', 'Baumwolle', 'Modal', 'Polyamid']
        materials = [ val for (index, val) in self.conn.cursor().execute('select * from Material;').fetchall() ]
        expected_colours = ['dazzling blue', 'ecru', 'noir']
        colours = [ val for (index, val) in self.conn.cursor().execute('select * from Colour;').fetchall() ]

        self.assertEqual(2, clothing_count, 'actual count is %d, shoud be 1'%clothing_count)
        self.assertEqual(expected_materials, materials, 'expected %s, got %s' % (expected_materials, materials))
        self.assertEqual(expected_colours, colours, 'expected %s, got %s' % (expected_colours, colours))


class VectorCreatorTestCase(unittest.TestCase):

    def setUp(self):
        global test_description_1
        global test_description_2
        self.conn = get_database()
        self.dm = get_database_manager(self.conn)
        self.cm = self.dm.get_clothing_manager()
        self.cm.add_document(create_clothing(test_description_1))
        self.cm.add_document(create_clothing(test_description_2))
        self.vm = self.dm.get_clothing_vector_manager()


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
            'Bluse': 1,
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
        
def get_database_manager(conn):
    return informationretrieval.DatabaseManager(conn)


def get_database():
    conn = sqlite3.connect(':memory:')
    return conn


create_clothing_count = 0
def create_clothing(description):
    """
def create_clothing(attribute_dict=None):
    global create_clothing_count
    ccc = create_clothing_count
    if not attribute_dict:
        attribute_dict = {}
    if not 'image_name' in attribute_dict:
        attribute_dict['image_name'] = 'image_%d' % ccc
    if not 'brand' in attribute_dict:
        attribute_dict['brand'] = 'brand_%d' % ccc
    if not 'cloth_type' in attribute_dict:
        attribute_dict['cloth_type'] = 'cloth_type_%d' % ccc
    if not 'colours' in attribute_dict:
        attribute_dict['colours'] = 'colour_%d' % ccc
    if not 'price' in attribute_dict:
        attribute_dict['price'] = 'price_%d' % ccc
    if not 'collar_type' in attribute_dict:
        attribute_dict['collar_type'] = 'collar_type_%d' % ccc
    if not 'materials' in attribute_dict:
        attribute_dict['materials'] = 'materials_%d' % ccc
    create_clothing_count += 1
    return informationretrieval.product.ProductCreator.create_debug_clothing(attribute_dict)
    """
    return informationretrieval.product.ProductCreator.create_clothing(description)

if __name__ == '__main__':
    print('hi')
    unittest.main()

