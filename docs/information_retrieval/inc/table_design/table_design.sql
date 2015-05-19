
PRAGMA foreign_keys = ON;

CREATE TABLE Clothing
(
    clothing_id     INTEGER PRIMARY KEY,
    image_name      TEXT UNIQUE NOT NULL,
    brand           TEXT,
    price           REAL,
    cloth_type      TEXT
);

CREATE TABLE Material
(
    material_id     INTEGER PRIMARY KEY,
    name            TEXT UNIQUE NOT NULL
);

CREATE TABLE Colour
(
    colour_id       INTEGER PRIMARY KEY,
    name            TEXT UNIQUE NOT NULL
);

CREATE TABLE ClothingMaterialAssigner
(
    clothing_id     INTEGER,
    material_id     INTEGER,

    PRIMARY KEY(clothing_ID, material_id),

    FOREIGN KEY(clothing_id) REFERENCES Clothing(clothing_id),
    FOREIGN KEY(material_id) REFERENCES Material(material_id)
);

CREATE TABLE ClothingColourAssigner
(
    clothing_id     INTEGER,
    colour_id       INTEGER,

    PRIMARY KEY(clothing_id, colour_id),

    FOREIGN KEY(clothing_id) REFERENCES Clothing(clothing_id),
    FOREIGN KEY(colour_id) REFERENCES Colour(colour_id)
);

CREATE INDEX IF NOT EXISTS clothing_material_assigner_index ON ClothingMaterialAssigner (clothing_id);
CREATE INDEX IF NOT EXISTS clothing_colour_assigner_index ON ClothingColourAssigner (clothing_id);
