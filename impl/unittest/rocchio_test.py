
import unittest
import math
import sqlite3

import recommender

test_description_blouse_1 = 'http://i1.ztat.net/large/4E/M2/1E/00/0K/11/4EM21E000-K11@4.jpg Emoi en Plus Bluse - dazzling blue 24,95 € 50 cm 70 cm bei Größe 44 Rundhals 100% Polyester'

test_description_blouse_2 = 'http://i2.ztat.net/large/NA/52/1D/03/NA/11/NA521D03N-A11@3.jpg NAF NAF WENT - Bluse - ecru/noir 38,95 €  55 cm bei Größe S Rundhals 64% Viskose, 22% Baumwolle, 10% Modal, 4% Polyamid'

test_description_trouser_1 = 'http://i1.ztat.net/large/DI/62/2X/00/Q8/58/DI622X00Q-858@1.1.jpg Dickies SLIM STRAIGHT WORK PANT - Chino - schwarz 54,95 € 79 cm bei Größe 32/32 103 cm bei Größe 32/32 verdeckter Zip-Fly Gesäßtaschen normal 65% Polyester, 35% Baumwolle'

test_description_trouser_2 = 'http://i1.ztat.net/large/NI/12/2J/04/5C/00/NI122J045-C00@6.jpg Nike Sportswear VENOM - Trainingshose - dark grey 69,95 € 82 cm bei Größe M 110 cm bei Größe M  Seitentaschen, Gesäßtaschen  100% Baumwolle'


class RocchioTest(unittest.TestCase):

    def setUp(self):
        self.vc = recommender.vector.debug.DebugVectorCreator()

        pass

    def tearDown(self):
        pass


    def test_calculate(self):

        k = 3

        orig = self.vc.get_vector()
        relevant_1 = self.vc.get_vector()
        relevant_2 = self.vc.get_vector()
        relevant_3 = self.vc.get_vector()
        non_relevant_1 = self.vc.get_vector()
        non_relevant_2 = self.vc.get_vector()
        non_relevant_3 = self.vc.get_vector()
        non_relevant_4 = self.vc.get_vector()


        # original user-vector
        orig.add_value(2)
        orig.add_value(6)
        orig.add_value(3)

        # relevant vectors
        relevant_1.add_value(3)
        relevant_1.add_value(2)
        relevant_1.add_value(4)

        relevant_2.add_value(3)
        relevant_2.add_value(3)
        relevant_2.add_value(3)

        relevant_3.add_value(1)
        relevant_3.add_value(2)
        relevant_3.add_value(3)


        # non-relevant vectors
        non_relevant_1.add_value(1)
        non_relevant_1.add_value(6)
        non_relevant_1.add_value(9)

        non_relevant_2.add_value(2)
        non_relevant_2.add_value(0)
        non_relevant_2.add_value(5)

        non_relevant_3.add_value(7)
        non_relevant_3.add_value(6)
        non_relevant_3.add_value(3)

        non_relevant_4.add_value(9)
        non_relevant_4.add_value(6)
        non_relevant_4.add_value(9)


        q_0 = orig
        list_d_related = [relevant_1, relevant_2, relevant_3]
        list_d_unrelated = [non_relevant_1, non_relevant_2, non_relevant_3, non_relevant_4]

        """
        constant = recommender.rocchio.RocchioConstant()
        constant.a = 1
        constant.b = 0.8
        constant.c = 0.1
        """
        constant = (1, 0.8, 0.1)

        result = recommender.rocchio.calculate(q_0, list_d_related, list_d_unrelated, constant)

        """
        origin_vector * RochioConstant.A
            (2,6,3) * 1 = (2,6,3)

        SUM( ((3,2,4), (3,3,3), (1,2,3))*(1/3)) * 0.8
            = ((7,7,10) * 1/3) * 0.8
            = (
                7 * (1/3) * 0.8,
                7 * (1/3) * 0.8,
                10 * (1/3) * 0.8
            )

        SUM(((1,6,9), (2,0,5), (7,6,3), (9,6,9) ) /(1/4)) * 0.1
            = ((19, 18, 26) / (1/4)) * 0.1
            = (4.75, 4.5, 6.5) * 0.1
            = (0.475, 0.45, 0.65)
        """

        expected = (
            2 + (7/3*0.8) - 0.475,
            6 + (7/3*0.8) - 0.45,
            3 + (10/3*0.8) - 0.65
        )

        # do not compare floats directly
        tolerance = 0.00001
        #print('result: %s' % str(result.values))
        #print('expected: %s' % str(expected))
        self.assertTrue(abs(result.values[0] - expected[0]) < tolerance)
        self.assertTrue(abs(result.values[1] - expected[1]) < tolerance)
        self.assertTrue(abs(result.values[2] - expected[2]) < tolerance)
        

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

