
import math

def add(a, b):
    """
    Adds stuff
    """
    return a + b;

def substract(a, b):
    """
    substracts stuff
    """
    return a - b;

def scalar_multiplication(vector, scalar):
    """
    multiplicates stuff
    """
    return vector.scalar_multiplication(scalar)

def absolute_value(vector):
    """Returns the absolute value of a vector.

    It is calculated by the
    euclidean norm ``abs(a) = Sqrt( pow(a1) + pow(a2) + pow(a3) )``

    :param vector: vector.abstractvector.DocumentVector
    :type vector: the vector whose absolute value will be calculated
    :returns: int
    """
    values = [ v for v in vector.values ]
    square_values = [ v**2 for v in values]
    absolute_value = math.sqrt(sum(square_values))
    return absolute_value
    pass

def primitive_distance(v1, v2):
   return absolute_value(v1 - v2)

def hamming_distance(v1, v2):
    return v1.hamming_distance(v2)

def euclidean_distance(v1, v2):
    return v1.euclidean_distance(v2)

#default_distance = hamming_distance
default_distance = euclidean_distance

def k_nearest_neighbours(k, vector_origin, vectors, distance_function=default_distance):
    distances = [(distance_function(vector_origin, v), v) for v in vectors]
    ratings = distances
    ratings.sort()
    return [(r, v) for (r, v) in ratings[:k] ]





