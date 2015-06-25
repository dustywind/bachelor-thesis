
import unittest
import sqlite3

import informationretrieval

test_description_1 = 'http://i1.ztat.net/large/4E/M2/1E/00/0K/11/4EM21E000-K11@4.jpg Emoi en Plus Bluse - dazzling blue 24,95 € 50 cm 70 cm bei Größe 44 Rundhals 90% Polyester, 10% Hamsterleder'

test_description_2 = 'http://i1.ztat.net/large/S3/62/1D/00/0B/11/S3621D000-B11@2.jpg See u Soon Bluse - beige 54,95 € 37 cm 61 cm bei Größe 36 Rundhals 55% Baumwolle, 45% Polyamid'

class ClothingImportTestCase(unittest.TestCase):

    def setUp(self):
        self.conn = get_database()
        self.dm = get_database_manager(self.conn)
        self.cm = self.dm.get_clothing_manager()

    def tearDown(self):
        self.conn.close()

    def test_import_1(self):
        global test_description_1
        c = create_clothing(test_description_1)
        self.cm.add_document(c)
        c = create_clothing(test_description_2)
        self.cm.add_document(c)

        clothing_count = len(self.conn.cursor().execute('select * from Clothing;').fetchall())
        expected_materials = ['Polyester', 'Hamsterleder', 'Baumwolle', 'Polyamid']
        materials = [ val for (index, val) in self.conn.cursor().execute('select * from Material;').fetchall() ]
        expected_colours = ['dazzling blue', 'beige']
        colours = [ val for (index, val) in self.conn.cursor().execute('select * from Colour;').fetchall() ]

        self.assertEqual(2, clothing_count, 'actual count is %d, shoud be 1'%clothing_count)
        self.assertEqual(expected_materials, materials, 'expected %s, got %s' % (expected_materials, materials))
        self.assertEqual(expected_colours, colours, 'expected %s, got %s' % (expected_colours, colours))

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

