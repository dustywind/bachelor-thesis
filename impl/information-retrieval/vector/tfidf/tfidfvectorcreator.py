
from . import TfIdfVector
from ..abstractvector import VectorCreatorFabric

class TfIdfVectorCreator(VectorCreatorFabric):
    
    def __init__(self):
        raise NotImplementedError()
        pass

    def create_vector(self):
        raise NotImplementedError()
