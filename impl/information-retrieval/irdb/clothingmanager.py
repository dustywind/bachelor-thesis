
import sqlite3

from documentmanager import DocumentManager

class ClothingManager(DocumentManager):

    def __init__(self, dbconn):
        self.__conn = dbconn

    def add_document(self, clothing):
        try:
            self.__insert_clothing(clothing)
            clothing.document_id = self.__get_id_of_clothing(clothing)
            self.__assign_colour(clothing.get_colours(), clothing.document_id)

            self.__assign_material(clothing.get_materials(), clothing.document_id)
        except Exception:
            self.__conn.rollback()
            raise Exception(sys.exc_info())
        else:
            self.__conn.commit()

    def __insert_clothing(self, clothing):
        c = self.__conn.cursor()
        parameters = {
            "image_name": clothing.get_image_name(),
            "brand": clothing.get_brand(),
            "price": clothing.get_price(),
            "cloth_type": clothing.get_cloth_type()
        }
        c.execute(
            '''
            INSERT INTO Clothing
            VALUES (null, :image_name, :brand, :price, :cloth_type);
            ''',
            parameters
        )

    def __get_id_of_clothing(self, clothing):
        c = self.__conn.cursor()
        image_name = clothing.get_image_name()
        parameters = {"image_name": image_name}
        c = c.execute(
            '''
            SELECT  document_id
            FROM    Clothing
            WHERE   image_name = :image_name
            ''', parameters
        )
        r = c.fetchone()
        assert r is not None

        return r[0]

    def __assign_colour(self, colours, clothing_id):
        c = self.__conn.cursor()

        colour_ids = [self.__get_or_create_colour_id(colour) for colour in colours]

        for colour in colour_ids:
            parameters = {"clothing_id": clothing_id, "colour_id": colour}
            c.execute(
                '''
                INSERT INTO ClothingColourAssigner
                VALUES (:clothing_id, :colour_id)
                ''', parameters
            )
            pass
        pass

    def __get_or_create_colour_id(self, colour_name):
        colour_id = None
        colour_id = self.__get_colour_id(colour_name)
        if not colour_id:
            self.__insert_colour(colour_name)
            colour_id = self.__get_colour_id(colour_name)
        return colour_id

    def __get_colour_id(self, colour_name):
        c = self.__conn.cursor()
        parameters = {"colour_name": colour_name}
        c.execute(
            '''
            SELECT  colour_id
            FROM    Colour
            WHERE   name = :colour_name;
            ''', parameters
        )
        row = c.fetchone()
        if not row:
            return None
        else:
            return row[0]
        pass

    def __insert_colour(self, colour_name):
        c = self.__conn.cursor()
        parameters = {"colour_name": colour_name}
        c.execute(
            '''
            INSERT INTO Colour
            VALUES (null, :colour_name);
            ''', parameters
        )
        pass


    def __assign_material(self, materials, clothing_id):
        material_ids = [self.__get_or_create_material_id(m) for m in materials]
        c = self.__conn.cursor()
        for material_id in material_ids:
            parameters = {"clothing_id": clothing_id, "material_id": material_id}
            c.execute(
                '''
                INSERT INTO ClothingMaterialAssigner
                VALUES (:clothing_id, :material_id)
                ''', parameters
            )
            pass
        pass

    def __get_or_create_material_id(self, material_name):
        material_id = None
        material_id = self.__get_material_id(material_name)
        if not material_id:
            self.__insert_material(material_name)
            material_id = self.__get_material_id(material_name)
        return material_id

    def __get_material_id(self, material_name):
        c = self.__conn.cursor()
        parameters = {"material_name": material_name}
        c.execute(
            '''
            SELECT  material_id
            FROM    Material
            WHERE   name = :material_name;
            ''', parameters
        )
        row = c.fetchone()
        if not row:
            return None
        else:
            return row[0]
        pass

    def __insert_material(self, material_name):
        c = self.__conn.cursor()
        parameters = {"material_name": material_name}
        c.execute(
            '''
            INSERT INTO Material
            VALUES (null, :material_name);
            ''', parameters
        )
        pass
