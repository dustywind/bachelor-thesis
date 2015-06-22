
from ..dependency import Dependency

class DocumentManager(Dependency):

    def add_document(self, document):
        raise NotImplementedError('This is an abstract method!')

    def build_dependencies():
        raise NotImplementedError('Must be implemented by heirs')

