
import math
import pdb

class DocumentVector(object):
    """Abstract class that represents a Vector.

    .. warning::
        Do **not** directly initialize this class -- use inherited classes instead!
    """
    
    def __init__(self):
        self.document_id = None
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

    def clone(self):
        """Clones the current Vector

        :returns: a new instance of an Vector with exactly the same values
        """
        # concatenating a tuple with an empty one creates a new one!
        # we do not want that changes on the original to also change the vector
        instance = self._get_new_instance()
        instance.term_id = self.term_id + ()
        instance.description = self.description()
        instance.values = self.values + ()
        return instance

    def _get_new_instance(self):
        """Create an instance of the current type

        :returns: an instance of the current type (something inherited by :class:`recommender.vector.abstractvector.DocumentVector`)
        """
        vector_class = self.__class__
        instance = vector_class()
        return instance

    def add_to_vector(self, triple):
        """Expands the vector for the given value.

        :param triple: an id, description and a value that shall be appended on the vector
        :type triple: tuple(int, str, float)
        """
        self.term_id = self.term_id + (triple[0],)
        self.description = self.description + (triple[1],)
        self.values = self.values + (triple[2],)
        pass

    def _get_content(self):
        return zip(self.term_id, self.description, self.values)

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

    def as_dictionary(self):
        d = {}
        d['document_id'] = self.document_id
        d['term_id'] = self.term_id
        d['description'] = self.description
        d['values'] = self.values
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
        if not len(self) == len(other):
            raise ValueError('the vectors are not compatible')

        values = tuple([ a + b for (a, b) in zip(self.values, other.values)])
        return DocumentVector._create(self.term_id, self.description, values)

    def __radd__(self, other):
        # by using the sum()-builtin the first entry of the list will be added to numeric zero
        if other == 0:
            return self
        return self.__add__(other)
        pass

    def __sub__(self, other):
        """Substract a vector to the current one.

        :returns: DocumentVector -- a **new** vector that represents the differential of the two vectors (no references to the old values)
        :raises: TypeError, ValueError
        """
        if not isinstance(other, DocumentVector):
            raise TypeError('unsupported operand type(s) for -: \'%s\' and \'%s\'' \
                % (self.__class__.__name__, other.__class__.__name__))
            pass
        if not len(self) == len(other):
            raise ValueError('the vectors are not compatible')

        values = tuple([ a - b for (a, b) in zip(self.values, other.values)])
        return DocumentVector._create(self.term_id, self.description, values)

    def __lt__(self, other):
        return self.document_id < other.document_id

    def __lt__(self, other):
        return self.document_id <= other.document_id

    def __gt__(self, other):
        return self.document_id > other.document_id

    def __gt__(self, other):
        return self.document_id >= other.document_id

    def __eq__(self, other):
        return self.document_id == other.document_id

    def scalar_multiplication(self, scalar):
        """Multiplicate the vector with a given scalar

        :parameter scalar: the scalar with which the vector will be multiplicated
        :type scalar: float
        :returs: DocumentVector -- a **new** vector (no references to the old values)
        """
        if not isinstance(scalar, int) and not isinstance(scalar, float):
            raise TypeError('unsupported operand type(s) for -: \'%s\' and \'%s\'' \
                % (self.__class__.__name__, scalar.__class__.__name__))
            pass

        values = tuple([scalar * v for v in self.values])
        return DocumentVector._create(self.term_id, self.description, values)

    def hamming_distance(self, other):
        distance = 0
        for val1, val2 in zip(self.values, other.values):
            if not val1 == val2:
                distance += 1
        return distance

    def euclidean_distance(self, other):
        t = sum(
            ((v1 - v2) ** 2  for v1, v2 in zip(self.values, other.values))
        )
        d = math.sqrt(t)
        return d















