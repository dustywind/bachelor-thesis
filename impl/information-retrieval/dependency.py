
from .databasemanager import DatabaseManager

class Dependency(object):
    
    def __init__(self, database_manager):
        self._database_manager = database_manager
        self.build_dependencies()

    def build_dependencies():
        raise NotImplementedError()
