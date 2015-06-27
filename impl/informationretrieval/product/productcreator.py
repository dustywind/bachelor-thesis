
import sys
import re

from .product import Product

class ProductCreator(object):

    __clothing_regex = re.compile('(http://i[12]\.ztat\.net[a-zA-Z\/0-9-@]*(?:\.?[0-9]?\.jpg)) (?:([a-zA-Z&\u00fc\. ]*) - ([a-zA-Z ]*)|([a-zA-Z&\u00fc\.\s]*) (Bluse))\s-\s([a-zA-Z\u00df\-\/ ]*) ([0-9, ]*) \u20ac ? (?:[0-9]{2}(?: cm) ){1,2}(?:bei|in) Gr\u00f6\u00dfe (?:(?:EU )?[0-9]{1,2}|[A-Z]{1,3}) ([a-zA-Z -]*) ((?:[0-9]{1,3}% [a-zA-Z]*(?:, )?)+)')

    @staticmethod
    def create_from_description(description):
        clothing = Clothing()
        match = Clothing.__clothing_regex.match(description)

        if not match:
            raise ValueError(description)

        clothing.image_name = self._get_image_name_from_match(match)

        clothing.add_term(self._get_brand_from_match(match))
        clothing.add_term(self._get_cloth_type_from_match(match))
        clothing.add_term(self._get_price_from_match(match))
        clothing.add_term(self._get_collar_type_from_match(match))

        for material in self.get_materials_from_match(match):
            clothing.add_term(material)
            pass
        for colour in self.get_colours_from_match(match):
            clothing.add_term(colour)
            pass
        return clothing

    @staticmethod
    def create_from_dictionary(attribute_dict, image_name=None):
        clothing = Clothing()

        if image_name is not None:
            clothing.image_name = image_name
        clothing.term = attribute_dict
        pass


    @staticmethod
    def _get_image_name_from_match(self, match):
        url = match.group(1)
        url_parts = url.split('/')
        return url_parts[-1]
        
    @staticmethod
    def _get_brand_from_match(self, match):
        if not match.group(2):
            return match.group(4)
        else:
            return match.group(2)

    @staticmethod
    def _get_cloth_type_from_match(self, match):
        if not match.group(3):
            return match.group(5)
        else:
            return match.group(3)

    @staticmethod
    def _get_colours_from_match(self, match):
        colours = match.group(6)
        return [colour.strip() for colour in colours.split('/')]

    @staticmethod
    def _get_price_from_match(self, match):
        """
        returns the price in eurocents as int
        """
        return int(match.group(7).replace(',', ''))

    @staticmethod
    def _get_collar_type_from_match(self, match):
        return match.group(8)
    
    @staticmethod
    def _get_materials_from_match(self, match):
        """
        returns all materials (without any percent information
        """
        materials = match.group(9)
        r = re.compile('([a-zA-Z]*)')
        return [ m for m in r.findall(materials) if len(m) > 0]

