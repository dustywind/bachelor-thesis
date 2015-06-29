

from ..abstractvector import VectorCreator
from . import DebugVector

class DebugVectorCreator(VectorCreator):
    """Creates debug-vectors

    Inherits from :class:`recommender.vector.abstractvector.VectorCreatorFabric`

    :parameter sqlite3_connection: connection to a database build with :class:`recommender.vector.vectortablecreator.VectorTableCreator`
    :type sqlite3_connection: sqlite3.Connection
    :raises: TypeError
    """

    def __init__(self, _=None):
        pass

    def get_vector(self, _=None):
        """creates an debug vector

        Overwrites :func:`recommender.vector.abstractvector.VectorCreatorFabric.get_vector` to suppress caching

        :returns: an debug vector
        """
        return DebugVector()

