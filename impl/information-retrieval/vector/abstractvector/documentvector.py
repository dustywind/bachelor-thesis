
class DocumentVector(object):
    
    def __init__(self):
        self.term_id = tuple() 
        self.description = tuple()
        self.values = tuple() 

    def add_to_vector(self, triple):
        self.term_id = self.term_id + (triple[0],)
        self.description = self.description + (triple[1],)
        self.values = self.values + (triple[2],)
        pass

    def as_dictionary(self):
        d = {}
        for t in zip(self.term_id, self.values):
            d[t[0]] = t[1]
        return d
