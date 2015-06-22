

from ..abstractvector import VectorCreator
from . import DebugVector

class DebugVectorCreator(VectorCreator):

    def __init__(self, _=None):
        pass

    def get_vector(self, _=None):
        return DebugVector()

