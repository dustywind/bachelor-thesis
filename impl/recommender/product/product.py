
import sys
import re

from ..document import Document

class Product(Document):

    def __init__(self):
        super(Product, self).__init__()
        self.document_id = None
        self.image_name = None

    def __unicode__(self):
        return ('Product: %s' % (self.terms)).encode('utf-8')

    def as_dictionary(self):
        jd = {}
        jd['image_name'] = self.image_name
        jd['document_id'] = self.document_id
        jd['terms'] = self.terms
        return jd

