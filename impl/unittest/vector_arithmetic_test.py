
import unittest
import math
import sqlite3

import recommender

test_description_blouse_1 = 'http://i1.ztat.net/large/4E/M2/1E/00/0K/11/4EM21E000-K11@4.jpg Emoi en Plus Bluse - dazzling blue 24,95 € 50 cm 70 cm bei Größe 44 Rundhals 100% Polyester'

test_description_blouse_2 = 'http://i2.ztat.net/large/NA/52/1D/03/NA/11/NA521D03N-A11@3.jpg NAF NAF WENT - Bluse - ecru/noir 38,95 €  55 cm bei Größe S Rundhals 64% Viskose, 22% Baumwolle, 10% Modal, 4% Polyamid'

test_description_trouser_1 = 'http://i1.ztat.net/large/DI/62/2X/00/Q8/58/DI622X00Q-858@1.1.jpg Dickies SLIM STRAIGHT WORK PANT - Chino - schwarz 54,95 € 79 cm bei Größe 32/32 103 cm bei Größe 32/32 verdeckter Zip-Fly Gesäßtaschen normal 65% Polyester, 35% Baumwolle'

test_description_trouser_2 = 'http://i1.ztat.net/large/NI/12/2J/04/5C/00/NI122J045-C00@6.jpg Nike Sportswear VENOM - Trainingshose - dark grey 69,95 € 82 cm bei Größe M 110 cm bei Größe M  Seitentaschen, Gesäßtaschen  100% Baumwolle'


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


    def test_k_nearest_neighbours(self):

        k = 3

        v0 = self.vc.get_vector()
        v1 = self.vc.get_vector()
        v2 = self.vc.get_vector()
        v3 = self.vc.get_vector()
        v4 = self.vc.get_vector()

        origin = v0
        vectors = [v1,v2,v3,v4]

        v0.document_id = 0
        v0.add_value(2)
        v0.add_value(6)
        v0.add_value(3)

        v1.document_id = 1
        v1.add_value(3)
        v1.add_value(7)
        v1.add_value(4)

        v2.document_id = 2
        v2.add_value(3)
        v2.add_value(3)
        v2.add_value(3)

        v3.document_id = 3
        v3.add_value(1)
        v3.add_value(9)
        v3.add_value(8)

        v4.document_id = 4
        v4.add_value(2)
        v4.add_value(6)
        v4.add_value(3)

        
        hamming_result = recommender.vector.arithmetic.k_nearest_neighbours(
            k,
            origin,
            vectors,
            recommender.vector.arithmetic.hamming_distance
        )

        hamming_result_vectors = [ v for r,v in hamming_result]

        expected_hamming_result = [v4,v2,v1]

        euclidean_result = recommender.vector.arithmetic.k_nearest_neighbours(
            k,
            origin,
            vectors,
            recommender.vector.arithmetic.euclidean_distance
        )

        euclidean_result_vectors = [ v for r,v in euclidean_result]

        expected_euclidean_result = [v4,v1,v2]

        self.assertEqual(expected_hamming_result, hamming_result_vectors)
        self.assertEqual(expected_euclidean_result, euclidean_result_vectors)

        pass
    
        
def get_database_manager(conn):
    return recommender.DatabaseManager(conn)


def get_database():
    tmp_database = "./1243889fduz9f892u39q8.sqlite3"
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

