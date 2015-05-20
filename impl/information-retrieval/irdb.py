
import os
import sqlite3
import sys

'''
information retrieval database connector
'''

class TableCreator:
    """
    Creates tables as defined in /docs/information_retrieval/ir_info
    """

    def __init__(self, db_path, db_name):
        self._db_path = db_path
        self._db_name = db_name
        self._db_full_path = os.path.join(db_path, db_name)

        self.__connect_to_db()
        pass

    def __del__(self):
        self.__close_db()

    def __connect_to_db(self):
        """
        Opens a connection to the given database
        """
        try:
            self.__conn = sqlite3.connect(self._db_full_path)
            c = self.__conn.cursor()
            c.execute('PRAGMA foreign_keys=ON')
        except Exception:
            self.__conn.rollback()
            raise Exception(sys.exc_info())
        else:
            self.__conn.commit()

    def __close_db(self):
        """
        Closes the connection to the database
        """
        self.__conn.close()

    def create_tables(self):
        self.__create_table_clothing()
        self.__create_table_material()
        self.__create_table_colour()
        self.__create_table_clothingmaterialassigner()
        self.__create_table_clothingcolourassigner()

    def __create_table_clothing(self):
        c = self.__conn.cursor()
        try:
            c.execute(
                '''
                CREATE TABLE IF NOT EXISTS Clothing
                (
                    clothing_id     INTEGER PRIMARY KEY,
                    image_name      TEXT UNIQUE NOT NULL,
                    brand           TEXT,
                    price           INTEGER,
                    cloth_type      TEXT
                );
                '''
            )
        except Exception:
            self.__conn.rollback()
            raise Exception(sys.exc_info())
        else:
            self.__conn.commit()

    def __create_table_material(self):
        c = self.__conn.cursor()
        try:
            c.execute(
                '''
                CREATE TABLE IF NOT EXISTS Material
                (
                    material_id     INTEGER PRIMARY KEY,
                    name            TEXT UNIQUE NOT NULL
                );
                '''
            )
        except Exception:
            self.__conn.rollback()
            raise Exception(sys.exc_info())
        else:
            self.__conn.commit()
    
    def __create_table_colour(self):
        c = self.__conn.cursor()
        try:
            c.execute(
                '''
                CREATE TABLE IF NOT EXISTS Colour
                (
                    colour_id       INTEGER PRIMARY KEY,
                    name            TEXT UNIQUE NOT NULL
                );
                '''
            )
        except Exception:
            self.__conn.rollback()
            raise Exception(sys.exc_info())
        else:
            self.__conn.commit()

    def __create_table_clothingmaterialassigner(self):
        c = self.__conn.cursor()
        try:
            c.execute(
                '''
                CREATE TABLE IF NOT EXISTS ClothingMaterialAssigner
                (
                    clothing_id     INTEGER,
                    material_id     TEXT UNIQUE NOT NULL,

                    PRIMARY KEY(clothing_id, material_id)

                    FOREIGN KEY(clothing_id) REFERENCES Clothing(clothing_id),
                    FOREIGN KEY(material_id) REFERENCES Material(material_id)
                );
                '''
            )
            c.execute(
                '''
                CREATE INDEX IF NOT EXISTS clothing_material_assigner_index
                ON ClothingMaterialAssigner(material_id);
                '''
            )
        except Exception:
            self.__conn.rollback()
            raise Exception(sys.exc_info())
        else:
            self.__conn.commit()

    def __create_table_clothingcolourassigner(self):
        c = self.__conn.cursor()
        try:
            c.execute(
                '''
                CREATE TABLE IF NOT EXISTS ClothingColourAssigner
                (
                    clothing_id     INTEGER,
                    colour_id       TEXT UNIQUE NOT NULL,

                    PRIMARY KEY(clothing_id, colour_id)

                    FOREIGN KEY(clothing_id) REFERENCES Clothing(clothing_id),
                    FOREIGN KEY(colour_id) REFERENCES Colour(colour_id)
                );
                '''
            )
            c.execute(
                '''
                CREATE INDEX IF NOT EXISTS clothing_colour_assigner_index
                ON ClothingColourAssigner(clothing_id);
                '''
            )
        except Exception:
            self.__conn.rollback()
            raise Exception(sys.exc_info())
        else:
            self.__conn.commit()

    def drop_tables(self):
        raise NotImplementedError()

    def recreate_tables(self):
        self.drop_tables()
        self.create_tables()

    def get_clothing_handler(self):
        return _ClothingHandler(self.__conn)


class _ClothingHandler:

    def __init__(self, conn):
        self.__conn = conn

    def add_clothing(self, clothing):
        try:
            self.__insert_clothing(clothing)
            clothing_id = self.__get_id_of_clothing(clothing)
            self.__assign_colour(clothing.get_colours(), clothing_id)
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
            SELECT  clothing_id
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
