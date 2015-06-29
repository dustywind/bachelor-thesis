"""Some comment
"""
#from . import DatabaseManager

class Dependency(object):
    """This class will be used to build dependencies amongst different Managers.
    These dependencies can for example be tables in a database.

    :param database_manager: a instance of a database_manager. The database_manager *must* provide a function to build the dependencies for the class inheriting ``Dependency``
    :type database_manager: recommender.DatabaseManager
    """

    def __init__(self, database_manager):
        self._database_manager = database_manager
        self.build_dependencies()

    def build_dependencies(self):
        """This method can be used to ensure that all necessarry preparations for using the inheriting class are made.
        """
        raise NotImplementedError()
