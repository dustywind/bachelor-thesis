
class DocumentVector(object):
    
    def __init__(self):
        self.description = ()
        self.values = ()

    def as_dictionary(self):
        d = {}
        for t in zip(self.description, self.values):
            d[t[0]] = t[1]
        return d
