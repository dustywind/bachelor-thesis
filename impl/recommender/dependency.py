"""Some comment
"""
#from . import DatabaseManager

class Dependency(object):
    """Dependency description
    """
    

    def __init__(self, database_manager):
        self._database_manager = database_manager
        self.build_dependencies()

    def build_dependencies(self):
        """Dependency.build_dependencies()
        """
        raise NotImplementedError()
