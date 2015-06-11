
class DocumentVector(object):
    
    def __init__(self):
        self.term_id = () 
        self.description = ()
        self.values = () 

    @staticmethod
    def _create(term_id_tuple, description_tuple, values_tuple):
        created = DocumentVector()
        # concatenating a tuple with an empty one creates a new one!
        # we do not want that changes on the original to also change the vector
        created.term_id = term_id_tuple + ()
        created.description = description_tuple + ()
        created.values = values_tuple + ()
        return created

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

    def _is_valid_vector(self):
        return len(self.values) == len(self.description) and len(self.values) == len(self.term_id)

    def __len__(self):
        return len(self.values)

    def __add__(self, other):
        if not isinstance(other, DocumentVector):
            raise TypeError('unsupported operand type(s) for +: \'%s\' and \'%s\'' \
                % (self.__class__.__name__, other.__class__.__name__))
            pass
        if not len(self) is len(other):
            raise ValueError('the vectors are not compatible')

        values = tuple([ a + b for (a, b) in zip(self.values, other.values)])
        return DocumentVector._create(self.term_id, self.description, values)

    def __sub__(self, other):
        if not isinstance(other, DocumentVector):
            raise TypeError('unsupported operand type(s) for -: \'%s\' and \'%s\'' \
                % (self.__class__.__name__, other.__class__.__name__))
            pass
        if not len(self) is len(other):
            raise ValueError('the vectors are not compatible')

        values = tuple([ a - b for (a, b) in zip(self.values, other.values)])
        return DocumentVector._create(self.term_id, self.description, values)


    def scalar_multiplication(self, scalar):
        if not isinstance(scalar, int):
            raise TypeError('unsupported operand type(s) for -: \'%s\' and \'%s\'' \
                % (self.__class__.__name__, scalar.__class__.__name__))
            pass

        values = tuple([scalar * v for v in self.values])
        return DocumentVector._create(self.term_id, self.description, values)






