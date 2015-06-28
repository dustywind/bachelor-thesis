
class Document(object):

    def __init__(self):
        self.document_id = None
        self.terms = {}
    
    def has_document_id(self):
        return self.document is not None

    def add_term(self, term_name, count=1):
        if term_name in self.terms:
            self.terms[term_name] += count
        else:
            self.terms[term_name] = count
        pass
