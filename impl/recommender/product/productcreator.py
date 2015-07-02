
import sys
import re

from .product import Product

class ProductCreator(object):

    __lady_blouse_regex = re.compile('(http://i[12]\.ztat\.net[a-zA-Z\/0-9-@]*(?:\.?[0-9]?\.jpg)) (?:([a-zA-Z&\u00fc\. ]*) - ([a-zA-Z ]*)|([a-zA-Z&\u00fc\.\s]*) (Bluse))\s-\s([a-zA-Z\u00df\-\/ ]*) ([0-9, ]*) \u20ac ? (?:[0-9]{2}(?: cm) ){1,2}(?:bei|in) Gr\u00f6\u00dfe (?:(?:EU )?[0-9]{1,2}|[A-Z]{1,3}) ([a-zA-Z -]*) ((?:[0-9]{1,3}% [a-zA-Z]*(?:, )?)+)')

    __gentleman_trouser_regex = re.compile('(http://i[12]\.ztat\.net[a-zA-Z\/0-9-@]*(?:\.?[0-9]?\.jpg)) ([\w\s&Üéö!]*)(?: - )?([\wäöüÄÖÜ]*) - ([a-zA-Zß\/\s]*)(?:\s*)([0-9,]*) € (:?[\d ]*) cm bei Größe (:?[\w\d\/]*) (:?[\d ]*) cm bei Größe (:?[\w\d\/]*) ([\w\s,äöüÄÖÜß-]*) ([\d\w,% ]*)')


    @staticmethod
    def create_lady_blouse_from_description(description):
        match = ProductCreator.__lady_blouse_regex.match(description)
        if not match:
            raise ValueError(description)

        product = Product()

        product.image_name = ProductCreator._LadyBlouse.get_image_name_from_match(match)

        product.add_term(ProductCreator._LadyBlouse.get_brand_from_match(match))
        product.add_term(ProductCreator._LadyBlouse.get_cloth_type_from_match(match))
        product.add_term(ProductCreator._LadyBlouse.get_price_from_match(match))
        product.add_term(ProductCreator._LadyBlouse.get_collar_type_from_match(match))

        for material in ProductCreator._LadyBlouse.get_materials_from_match(match):
            product.add_term(material)
            pass
        for colour in ProductCreator._LadyBlouse.get_colours_from_match(match):
            product.add_term(colour)
            pass
        return product
    

    @staticmethod
    def create_gentleman_trouser_from_description(description):
        match = ProductCreator.__gentleman_trouser_regex.match(description)
        if not match:
            raise ValueError(description)

        product = Product()
        product.image_name = ProductCreator._GentlemanTrouser.get_image_name_from_match(match)

        product.add_term(ProductCreator._GentlemanTrouser.get_brand_from_match(match))
        product.add_term(ProductCreator._GentlemanTrouser.get_type_from_match(match))
        product.add_term(ProductCreator._GentlemanTrouser.get_price_from_match(match))


        for pocket_type in ProductCreator._GentlemanTrouser.get_pocket_types_from_match(match):
            product.add_term(pocket_type)

        for colour in ProductCreator._GentlemanTrouser.get_colours_from_match(match):
            product.add_term(colour)

        for material in ProductCreator._GentlemanTrouser.get_materials_from_match(match):
            product.add_term(material)
        return product


    @staticmethod
    def create_from_dictionary(attribute_dict, image_name=None):
        product = Clothing()

        if image_name is not None:
            product.image_name = image_name
        product.term = attribute_dict
        pass


    class _GentlemanTrouser(object):

        @staticmethod
        def get_image_name_from_url(url):
            url_parts = url.split('/')
            return url_parts[-1].strip()

        @staticmethod
        def get_image_name_from_match(match):
            url = match.group(1)
            return ProductCreator._LadyBlouse.get_image_name_from_url(url)

        @staticmethod
        def get_brand_from_match(match):
            brand = match.group(2).strip()
            return brand

        @staticmethod
        def get_type_from_match(match):
            cloth_type = match.group(3).strip()
            return cloth_type 

        @staticmethod
        def get_price_from_match(match):
            price = match.group(5).strip()
            return int(price.replace(',', ''))

        @staticmethod
        def get_pocket_types_from_match(match):
            pocket_types = match.group(10)
            return [pocket_type.strip() for pocket_type in pocket_types.split(',')]

        @staticmethod
        def get_materials_from_match(match):
            materials = match.group(11)
            return ProductCreator._GentlemanTrouser.get_materials_from_str(materials)
            raise NotImplementedError()

        @staticmethod
        def get_materials_from_str(materials):
            r = re.compile('([a-zA-Z]*)')
            return [ m for m in r.findall(materials) if len(m) > 0]

        @staticmethod
        def get_colours_from_match(match):
            colours = match.group(4)
            return [colour.strip() for colour in colours.split('/')]

        

    class _LadyBlouse(object):
        
        @staticmethod
        def get_image_name_from_url(url):
            url_parts = url.split('/')
            return url_parts[-1]
            pass

        @staticmethod
        def get_materials_from_str(materials):
            r = re.compile('([a-zA-Z]*)')
            return [ m for m in r.findall(materials) if len(m) > 0]

        @staticmethod
        def get_image_name_from_match(match):
            url = match.group(1)
            return ProductCreator._LadyBlouse.get_image_name_from_url(url)

        @staticmethod
        def get_brand_from_match(match):
            if not match.group(2):
                return match.group(4)
            else:
                return match.group(2)

        @staticmethod
        def get_cloth_type_from_match(match):
            if not match.group(3):
                return match.group(5)
            else:
                return match.group(3)

        @staticmethod
        def get_colours_from_match(match):
            colours = match.group(6)
            return [colour.strip() for colour in colours.split('/')]

        @staticmethod
        def get_price_from_match(match):
            """
            returns the price in eurocents as int
            """
            return int(match.group(7).replace(',', ''))

        @staticmethod
        def get_collar_type_from_match(match):
            return match.group(8)
        
        @staticmethod
        def get_materials_from_match(match):
            """
            returns all materials (without any percent information
            """
            materials = match.group(9)
            return ProductCreator._LadyBlouse.get_materials_from_str(materials)


