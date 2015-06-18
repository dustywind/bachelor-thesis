

from ..abstractvector import DocumentVector

class DebugVector(DocumentVector):

    def __init__(self):
        super(DebugVector, self).__init__()
        self.index_count = 0

    def add_value(self, value):
        self.add_to_vector((self.index_count, '', value))
        self.index_count += 1
        

