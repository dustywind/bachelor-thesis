
class DocumentVector(object):
    """Abstract class that represents a Vector.

    .. warning::
        Do **not** directly initialize this class -- use inherited classes instead!
    """
    
    def __init__(self):
        self.term_id = () 
        self.description = ()
        self.values = () 

    @staticmethod
    def _create(term_id_tuple, description_tuple, values_tuple):
        """Creates a fully developed vector from the values passed as parameter.

        :param term_id_tuple: tuple of term_ids
        :type term_id_tuple: tuple(int)
        :param description_tuple: tuple of descriptions
        :type description_tuple: tuple(str)
        :param values_tuple: tuple of values
        :type values_tuple: tuple(float)
        :returns: DocumentVector -- vector that represents the data from the parameter
        """
        created = DocumentVector()
        # concatenating a tuple with an empty one creates a new one!
        # we do not want that changes on the original to also change the vector
        created.term_id = term_id_tuple + ()
        created.description = description_tuple + ()
        created.values = values_tuple + ()
        return created

    def add_to_vector(self, triple):
        """Expands the vector for the given value.

        :param triple: an id, description and a value that shall be appended on the vector
        :type triple: tuple(int, str, float)
        """
        self.term_id = self.term_id + (triple[0],)
        self.description = self.description + (triple[1],)
        self.values = self.values + (triple[2],)
        pass

    def as_id_dictionary(self):
        """Creates a dictionary containing the term-id and the corresponding value.

        :returns: {'term_id': value} -- a dictionary with the term-ids and the corresponding value
        """
        d = {}
        for t in zip(self.term_id, self.values):
            d[t[0]] = t[1]
        return d

    def as_description_dictionary(self):
        """Creates a dictionary containing the description and the corresponding value.

        :returns: {'description': value} -- a dictionary with the descriptions and the corresponding value
        """
        d = {}
        for t in zip(self.description, self.values):
            d[t[0]] = t[1]
        return d

    def _is_valid_vector(self):
        """Rudimentary check if the vector is valid.

        It only checks, if the number of term-ids, descriptions and values is equal.

        :returns: bool -- true, if the vector seems to be ok

        """
        return len(self.values) == len(self.description) and len(self.values) == len(self.term_id)

    def __len__(self):
        """Get the number of values stored in the vector.

        :returns: (int) -- number of elements within the vector
        """
        return len(self.values)

    def __add__(self, other):
        """Add a vector to the current one.
        
        :returns: DocumentVector -- a **new** vector that represents the sum of the two vectors (no references to the old values)
        :raises: TypeError, ValueError
        """
        if not isinstance(other, DocumentVector):
            raise TypeError('unsupported operand type(s) for +: \'%s\' and \'%s\'' \
                % (self.__class__.__name__, other.__class__.__name__))
            pass
        if not len(self) is len(other):
            raise ValueError('the vectors are not compatible')

        values = tuple([ a + b for (a, b) in zip(self.values, other.values)])
        return DocumentVector._create(self.term_id, self.description, values)

    def __sub__(self, other):
        """Substract a vector to the current one.

        :returns: DocumentVector -- a **new** vector that represents the differential of the two vectors (no references to the old values)
        :raises: TypeError, ValueError
        """
        if not isinstance(other, DocumentVector):
            raise TypeError('unsupported operand type(s) for -: \'%s\' and \'%s\'' \
                % (self.__class__.__name__, other.__class__.__name__))
            pass
        if not len(self) is len(other):
            raise ValueError('the vectors are not compatible')

        values = tuple([ a - b for (a, b) in zip(self.values, other.values)])
        return DocumentVector._create(self.term_id, self.description, values)


    def scalar_multiplication(self, scalar):
        """Multiplicate the vector with a given scalar

        :parameter scalar: the scalar with which the vector will be multiplicated
        :type scalar: float
        :returs: DocumentVector -- a **new** vector (no references to the old values)
        """
        if not isinstance(scalar, int):
            raise TypeError('unsupported operand type(s) for -: \'%s\' and \'%s\'' \
                % (self.__class__.__name__, scalar.__class__.__name__))
            pass

        values = tuple([scalar * v for v in self.values])
        return DocumentVector._create(self.term_id, self.description, values)



