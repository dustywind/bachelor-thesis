
import sqlite3
import sys

from .documentmanager import DocumentManager
#from .. import DatabaseManager
from .clothingtablecreator import ClothingTableCreator

class ClothingManager(DocumentManager):

    def __init__(self, database_manager):
        super(ClothingManager, self).__init__(database_manager)
        self._conn = database_manager._conn

        table_creator = ClothingTableCreator(self._conn)
        table_creator.init_database()

    def build_dependencies(self):
        """has no dependencies
        """
        pass

    def add_document(self, clothing):
        try:
            self._insert_clothing(clothing)
            clothing.document_id = self._get_id_of_clothing(clothing)
            self._assign_colour(clothing.get_colours(), clothing.document_id)

            self._assign_material(clothing.get_materials(), clothing.document_id)
        except Exception:
            self._conn.rollback()
            raise Exception(sys.exc_info())
        else:
            self._conn.commit()

    def _insert_clothing(self, clothing):
        c = self._conn.cursor()
        parameters = {
            "image_name": clothing.get_image_name(),
            "brand": clothing.get_brand(),
            "price": clothing.get_price(),
            "cloth_type": clothing.get_cloth_type()
        }
        c.execute(
            '''
            INSERT OR IGNORE INTO Clothing
            VALUES (null, :image_name, :brand, :price, :cloth_type);
            ''',
            parameters
        )

    def _get_id_of_clothing(self, clothing):
        c = self._conn.cursor()
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

    def _assign_colour(self, colours, clothing_id):
        c = self._conn.cursor()

        colour_ids = [self._get_or_create_colour_id(colour) for colour in colours]

        for colour in colour_ids:
            parameters = {"clothing_id": clothing_id, "colour_id": colour}
            c.execute(
                '''
                INSERT OR IGNORE INTO ClothingColourAssigner
                VALUES (:clothing_id, :colour_id)
                ''', parameters
            )
            pass
        pass

    def _get_or_create_colour_id(self, colour_name):
        colour_id = None
        colour_id = self._get_colour_id(colour_name)
        if not colour_id:
            self._insert_colour(colour_name)
            colour_id = self._get_colour_id(colour_name)
        return colour_id

    def _get_colour_id(self, colour_name):
        c = self._conn.cursor()
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

    def _insert_colour(self, colour_name):
        c = self._conn.cursor()
        parameters = {"colour_name": colour_name}
        c.execute(
            '''
            INSERT OR IGNORE INTO Colour
            VALUES (null, :colour_name);
            ''', parameters
        )
        pass


    def _assign_material(self, materials, clothing_id):
        material_ids = [self._get_or_create_material_id(m) for m in materials]
        c = self._conn.cursor()
        for material_id in material_ids:
            parameters = {"clothing_id": clothing_id, "material_id": material_id}
            c.execute(
                '''
                INSERT OR IGNORE INTO ClothingMaterialAssigner
                VALUES (:clothing_id, :material_id)
                ''', parameters
            )
            pass
        pass

    def _get_or_create_material_id(self, material_name):
        material_id = None
        material_id = self._get_material_id(material_name)
        if not material_id:
            self._insert_material(material_name)
            material_id = self._get_material_id(material_name)
        return material_id

    def _get_material_id(self, material_name):
        c = self._conn.cursor()
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

    def _insert_material(self, material_name):
        c = self._conn.cursor()
        parameters = {"material_name": material_name}
        c.execute(
            '''
            INSERT OR IGNORE INTO Material
            VALUES (null, :material_name);
            ''', parameters
        )
        pass
