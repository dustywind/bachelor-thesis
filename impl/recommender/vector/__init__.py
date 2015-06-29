
"""
Vector-Packagage
This package contains all classes and functions revolving around Vectors
"""

from .productvectormanager import ProductVectorManager
from .vectormanager import VectorManager
from .vectortablecreator import VectorTableCreator
from .uservectormanager import UserVectorManager
from .usertablecreator import UserTableCreator

import recommender.vector.abstractvector
import recommender.vector.df
import recommender.vector.debug 
import recommender.vector.empty 
import recommender.vector.idf
import recommender.vector.user 
import recommender.vector.tfidf 
import recommender.vector.tf

from .arithmetic import *

