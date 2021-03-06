
import unittest
import math
import sqlite3

import recommender


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

