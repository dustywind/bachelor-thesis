
import sys
import re

from ..document import Document

class Product(Document):

    def __init__(self):
        super(Product, self).__init__()
        self.image_name = None

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return 'Product: %s' % (self.terms)

