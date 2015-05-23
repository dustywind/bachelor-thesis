
from product import Clothing

class ProductCreator(object):

    @staticmethod
    def create_clothing(description):
        return Clothing(description)
