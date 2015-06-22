
import sqlite3
import sys
import pdb

from ..irdb import TableCreator

class VectorTableCreator(TableCreator):
    """some comment"""

    def __init__(self, conn):
        self._conn = conn

    def init_database(self):
        try:
            self._create_tables()

            self._fill_tables()
        except Exception:
            self._conn.rollback()
            raise Exception(sys.exc_info())
        else:
            self._conn.commit()

    def _create_tables(self):
        """Creates all tables needed for the vectormodule
        """
        # the order is somewhat important to guarantee
        # referential integrity
        self._create_term_table()
        self._create_termdocumentassigner_table()
        self._create_n_view()
        """
        self._create_usermanagement_table()
        self._create_uservector_table()
        self._create_userpreference_table()
        """
        

    def _create_term_table(self):
        c = self._conn.cursor()
        c.execute(
            '''
            CREATE TABLE IF NOT EXISTS Term
            (
                term_id     INTEGER PRIMARY KEY,
                name        TEXT UNIQUE NOT NULL,
                datatype    TEXT NOT NULL
            );
            '''
        )
        pass

    def _create_termdocumentassigner_table(self):
        c = self._conn.cursor()
        c.execute(
            '''
            CREATE TABLE IF NOT EXISTS TermDocumentAssigner
            (
                term_id     INTEGER NOT NULL,
                document_id INTEGER NOT NULL,

                PRIMARY KEY(term_id, document_id),

                FOREIGN KEY(term_id) REFERENCES Term(term_id),
                FOREIGN KEY(document_id) REFERENCES Clothing(document_id)
            );
            '''
        )
        c.execute(
            '''
            CREATE INDEX IF NOT EXISTS
            term_document_assigner_index ON
            TermDocumentAssigner(document_id);
            '''
        )

    def _create_uservector_table(self):
        c = self._conn.cursor()
        c.execute(
            '''
            CREATE TABLE IF NOT EXISTS UserVector
            (
                user_id     INTEGER NOT NULL,
                term_id     INTEGER NOT NULL,
                value       REAL NOT NULL,

                PRIMARY KEY(user_id, term_id),

                FOREIGN KEY(term_id) REFERENCES Term(term_id),
                FOREIGN KEY(user_id) REFERNENCES UserManagement(user_id)
            );
            '''
        )
        pass
        
    def _create_usermanagement_table(self):
        c = self._conn.cursor()
        c.execute(
            '''
            CREATE TABLE IF NOT EXISTS UserManagement
            (
                user_id     INTEGER PRIMARY KEY,
                name        TEXT NOT NULL
            )
            ;
            '''
        )
        pass

    def _create_userpreference_table():
        c = self._conn.cursor()
        c.execute(
            '''
            CREATE TABLE IF NOT EXISTS UserPreference
            (
                user_id     INTEGER NOT NULL,
                document_id INTEGER NOT NULL,

                PRIMARY KEY(user_id, document_id),

                FOREIGN KEY(user_id) REFERENCES UserManagement(user_id),
                FOREIGN KEY(document_id) REFERENCES Clothing(document_id)
            )
            ;
            '''
        )
        pass

    def _create_n_view(self):
        c = self._conn.cursor()
        c.execute(
            '''
            CREATE VIEW IF NOT EXISTS N AS
            SELECT      (SELECT COUNT(*) FROM Clothing) AS document_count,
                        (SELECT COUNT(*) FROM Term) AS term_count
            ;
            '''
        )

    def _fill_tables(self):
        self._fill_with_clothing()
        self._fill_with_material()
        self._fill_with_colour()
        pass


    def _fill_with_clothing(self):
        c = self._conn.cursor()
        c.execute('''SELECT document_id, image_name, brand, price, cloth_type FROM Clothing;''')
        for row in c.fetchall():
            clothing = {'clothing_id': row[0],
                        'image_name': row[1],
                        'brand': row[2],
                        'price': row[3],
                        'cloth_type': row[4]}
            #self.add_to_term_table(clothing['clothing_id'], clothing['image_name'], 'TEXT')
            self.add_to_term_table(clothing['clothing_id'], clothing['brand'], 'TEXT')
            self.add_to_term_table(clothing['clothing_id'], clothing['price'], 'INTEGER')
            self.add_to_term_table(clothing['clothing_id'], clothing['cloth_type'], 'TEXT')

    def _fill_with_material(self):
        c = self._conn.cursor()
        c.execute(
            '''SELECT m.name, a.clothing_id
                FROM    Material AS m
                        INNER JOIN ClothingMaterialAssigner AS a
                        ON m.material_id = a.material_id
                ;
            '''
        )
        for row in c.fetchall():
            material = {'material_name': row[0], 'clothing_id': row[1]}
            self.add_to_term_table(material['clothing_id'], material['material_name'], 'TEXT')
        pass

    def _fill_with_colour(self):
        c = self._conn.cursor()
        c.execute(
            '''SELECT c.name, a.clothing_id
                FROM    Colour AS c
                        INNER JOIN ClothingColourAssigner AS a
                        ON c.colour_id = a.colour_id
                ;
            '''
        )
        for row in c.fetchall():
            colour = {'colour_name': row[0], 'clothing_id': row[1]}
            self.add_to_term_table(colour['clothing_id'], colour['colour_name'], 'TEXT')
        pass


    def add_to_term_table(self, clothing_id, term_name, datatype):
        c = self._conn.cursor()
        if not self.term_table_has_entry(term_name):
            c.execute(
                '''
                INSERT OR IGNORE INTO Term VALUES(null, :term_name, :datatype);
                ''', {'term_name': term_name, 'datatype': datatype}
            )
            pass

        parameter = {'term_id': self.get_term_id_from_term_name(term_name),
                    'document_id': clothing_id
        }
        c.execute(
            '''
            INSERT OR IGNORE INTO TermDocumentAssigner VALUES(:term_id, :document_id);
            ''', parameter
        )
        pass


    def term_table_has_entry(self, term_name):
        return self.get_term_id_from_term_name(term_name) is not None

    def get_term_id_from_term_name(self, term_name):
        c = self._conn.cursor()
        c.execute('''
            SELECT  term_id
            FROM    Term
            WHERE   name = :name;
            ''', {'name': term_name}
        )
        term_id = c.fetchone()
        if not term_id:
            return None
        else:
            return int(term_id[0])

