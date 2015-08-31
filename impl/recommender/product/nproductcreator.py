



import sys
import re

from .product import Product

class NProductCreator(object):

    __lady_blouse_regex = re.compile('http:\/\/(i[12]\.ztat\.net[a-zA-Z\/0-9-@]*\.?[a-zA-Z0-9]*?\.jpg) (.*)')

    __gentleman_trouser_regex = re.compile('http:\/\/(i[12]\.ztat\.net[a-zA-Z\/0-9-@]*\.?[0-9]?\.jpg) (.*)')


    @staticmethod
    def create_lady_blouse_from_description(description):
        match = NProductCreator.__lady_blouse_regex.match(description)
        if not match:
            raise ValueError(description)

        product = Product()

        product.image_name = url = match.group(1).replace('/', '')

        blob = match.group(2)
        for term in blob.split(' '):
            if len(term) > 0:
                product.add_term(term)

        return product

    @staticmethod
    def create_gentleman_trouser_from_description(description):
        match = NProductCreator.__gentleman_trouser_regex.match(description)
        if not match:
            raise ValueError(description)

        product = Product()

        product.image_name = url = match.group(1).replace('/', '')
        
        blob = match.group(2)
        for term in blob.split(' '):
            if len(term) > 0:
                product.add_term(term)
        return product

        
