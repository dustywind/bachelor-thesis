__author__ = 'dust'

import re

class Bluse:

    #__input_regex = re.compile(u'(http://i[12]\.ztat\.net[a-zA-Z\/0-9-@]*(?:\.[0-9]\.jpg|\.jpg)) (?:([a-zA-Z&\u00fc\. ]*) - ([a-zA-Z ]*)|([a-zA-Z&\u00fc\.\s]*) (Bluse))\s-\s([a-zA-Z\u00df\-\/ ]*) ([0-9, ]*) \u20ac ? (?:[0-9]{2}(?: cm) ){1,2}bei Gr\u00f6\u00dfe (?:(?:EU )?[0-9]{1,2}|[A-Z]{1,3}) ([a-zA-Z -]*) ((?:[0-9]{1,3}% [a-zA-Z]*(?:, )?)+)')

    __input_regex = re.compile(u'(http://i[12]\.ztat\.net[a-zA-Z\/0-9-@]*(?:\.?[0-9]?\.jpg)) (?:([a-zA-Z&\u00fc\. ]*) - ([a-zA-Z ]*)|([a-zA-Z&\u00fc\.\s]*) (Bluse))\s-\s([a-zA-Z\u00df\-\/ ]*) ([0-9, ]*) \u20ac ? (?:[0-9]{2}(?: cm) ){1,2}(?:bei|in) Gr\u00f6\u00dfe (?:(?:EU )?[0-9]{1,2}|[A-Z]{1,3}) ([a-zA-Z -]*) ((?:[0-9]{1,3}% [a-zA-Z]*(?:, )?)+)')

    def __init__(self, description):
        self.__description = description
        match = Bluse.__input_regex.match(self.__description)

        if not match:
            raise ValueError(description)

        self._image_name = self._get_image_name_from_match(match)
        self._brand = self._get_brand_from_match(match)
        self._cloth_type = self._get_cloth_type_from_match(match)
        self._colours = self._get_colours_from_match(match)
        self._price = self._get_price_from_match(match)
        self._collar_type = self._get_collar_type_from_match(match)
        self._materials = self._get_material_from_match(match)
        pass

    def _get_image_name_from_match(self, match):
        url = match.group(1)
        url_parts = url.split('/')
        return url_parts[-1]
        
    def _get_brand_from_match(self, match):
        if not match.group(2):
            return match.group(4)
        else:
            return match.group(2)

    def _get_cloth_type_from_match(self, match):
        if not match.group(3):
            return match.group(5)
        else:
            return match.group(3)

    def _get_colours_from_match(self, match):
        colours = match.group(6)
        return [colour.strip() for colour in colours.split('/')]

    def _get_price_from_match(self, match):
        """
        returns the price in eurocents as int
        """
        return int(match.group(7).replace(',', ''))

    def _get_collar_type_from_match(self, match):
        return match.group(8)
    
    def _get_material_from_match(self, match):
        """
        returns all materials (without any percent information
        """
        materials = match.group(9)
        r = re.compile('([a-zA-Z]*)')
        return [ m for m in r.findall(materials) if len(m) > 0]

    def get_image_name(self):
        return self._image_name

    def get_brand(self):
        return self._brand

    def get_cloth_type(self):
        return self._cloth_type

    def get_colours(self):
        return self._colours

    def get_price(self):
        return self._price

    def get_collar_type(self):
        return self._collar_type

    def get_materials(self):
        return self._materials

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u'%s, %s, %s, %s, %s, %s, %s' % (self._image_name, self._brand, self._cloth_type, self._colours, self._price, self._collar_type, self._materials)

