
"""
Vector-Packagage
This package contains all classes and functions revolving around Vectors
"""

from .clothingvectormanager import ClothingVectorManager
from .vectormanager import VectorManager
from .vectortablecreator import VectorTableCreator

import vector.abstractvector
import vector.documentfrequency
import vector.empty
import vector.inversedocumentfrequency
import vector.tfidf
import vector.termfrequency


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














