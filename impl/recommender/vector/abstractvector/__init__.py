
"""The abstract vector module builds the basis for all vectors build in this library.
Each of the vectors must be created by an incstance of :class:`recommender.vector.abstractvector.VectorCreator`.

.. moduleauthor:: dustywind
"""
import recommender.vector.abstractvector.documentvector
import recommender.vector.abstractvector.vectorcreator

from .documentvector import DocumentVector
from .vectorcreator import VectorCreator


