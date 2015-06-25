
from .clothing import Clothing

class ProductCreator(object):

    @staticmethod
    def create_clothing(description):
        #return Clothing(description)
        return Clothing.create_from_description(description)

    @staticmethod
    def create_debug_clothing(attribute_dict):
        return Clothing.create_from_dictionary(attribute_dict)
    
