
class Document(object):
    """A vessel for a document
    """

    def __init__(self):
        self.document_id = None
        self.terms = {}
    
    def has_document_id(self):
        """checks, if the document has a document_id

        :returns: true, if the Document-instance has a document_id
        """
        return self.document is not None

    def add_term(self, term_name, freq=1):
        """Adds a term and a frequency to the document

        :param term_name: the name of the term
        :type term_name: str
        :param freq: the frequency of the term within the document
        :type freq: int
        """
        if term_name in self.terms:
            self.terms[term_name] += count
        else:
            self.terms[term_name] = count
        pass
