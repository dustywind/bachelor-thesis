

from ..abstractvector import VectorCreatorFabric
from . import DebugVector

class DebugVectorCreator(VectorCreatorFabric):

    def __init__(self, _=None):
        pass

    def get_vector(self, _=None):
        return DebugVector()

