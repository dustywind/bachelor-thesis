
"""
Vector-Packagage
This package contains all classes and functions revolving around Vectors
"""

from .productvectormanager import ProductVectorManager
from .vectormanager import VectorManager
from .vectortablecreator import VectorTableCreator
from .uservectormanager import UserVectorManager
from .usertablecreator import UserTableCreator

import informationretrieval.vector.abstractvector
import informationretrieval.vector.documentfrequency
import informationretrieval.vector.debug
import informationretrieval.vector.empty
import informationretrieval.vector.inversedocumentfrequency
import informationretrieval.vector.user
import informationretrieval.vector.tfidf
import informationretrieval.vector.termfrequency

from .arithmetic import *

