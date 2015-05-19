
import os
import sqlite3
import sys

'''
information retrieval database connector
'''

class TableCreator:
    '''
    Creates tables as defined in /docs/information_retrieval/ir_info
    '''
    __clothing_table_name = 'Clothing'
    __material_table_name = 'Material'
    __colour_table_name = 'Colour'
    __clothingmaterialassigner_table_name = 'ClothingMaterialAssigner'
    __clothingcolourassigner_table_name = 'ClothingColourAssigner'

    def __init__(self, db_path, db_name):
        self._db_path = db_path
        self._db_name = db_name
        self._db_full_path = os.path.join(db_path, db_name)

        self.__connect_to_db()
        pass

    def __del__(self):
        self.__close_db()

    def __connect_to_db(self):
        '''
        Opens a connection to the given database
        '''
        self.__conn = sqlite3.connect(self._db_full_path)
        c = self.__conn.cursor()
        try:
            c.execute('PRAGMA foreign_keys=ON')
        except Exception, e:
            __conn.rollback()
            raise Exception(e)
        else:
            self.__conn.commit()

    def __close_db(self):
        '''
        Closes the connection to the database
        '''
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
        except Exception, e:
            self.__conn.rollback()
            raise Exception(e)
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
        except Exception, e:
            self.__conn.rollback()
            raise Exception(e)
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
        except Exception, e:
            self.__conn.rollback()
            raise Exception(e)
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
        except Exception, e:
            self.__conn.rollback()
            raise Exception(e)
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
        except Exception, e:
            self.__conn.rollback()
            raise Exception(e)
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
            print 'foo'
            clothing_id = self.__get_id_of_clothing(clothing)
            print clothing_id
            self.__insert_colour(clothing, clothing_id)
            print 'narf'
        except Exception, e:
            self.__conn.rollback()
            raise Exception(e)
        else:
            self.__conn.commit()

    def __insert_clothing(self, clothing):
        c = self.__conn.cursor()
        c.execute(
            '''
            INSERT INTO Clothing
            VALUES (null, ?, ?, ?, ?);
            ''',
            (
                clothing.get_image_name(),
                clothing.get_brand(),
                clothing.get_price(),
                clothing.get_cloth_type()
            )
        )
    def __get_id_of_clothing(self, clothing):
        c = self.__conn.cursor()
        c.execute(
            '''
            SELECT MAX(clothing_id) FROM Clothing;
            '''
        )
        return c.fetchone()[0]

    def __insert_colour(self, clothing, clothing_id):
        c = self.__conn.cursor()
        colour_ids = self.__get_colour_ids(clothing.get_colours())
        print colour_ids
        for colour in colour_ids:
            c.execute(
                '''
                INSERT INTO Colour
                VALUES (?, ?)
                ''', (clothing_id, colour_id)
            )
            pass

    def __get_colour_ids(self, colours):
        c = self.__conn.cursor()
        print clothing.get_colours()
        c.execute(
            '''
            SELECT  colour_id
            FROM    Colour
            WHERE   name IN (?);
            ''', colours
        )
        ids = []
        for colour_id in c:
            colour_ids.append(colour_id)
        return ids




















