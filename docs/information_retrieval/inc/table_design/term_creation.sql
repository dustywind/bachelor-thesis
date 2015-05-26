
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS Term 
(
    term_id         INTEGER PRIMARY KEY,
    value           TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS TermDocumentAssigner 
(
    term_id         INTEGER,
    document_id     INTEGER,

    PRIMARY KEY(term_id, document_id),

    FOREIGN KEY(term_id) REFERENCES Term(term_id),
    FOREIGN KEY(document_id) REFERENCES Clothing(document_id)
);

-- total number of documents
CREATE VIEW IF NOT EXISTS N AS
SELECT  COUNT(*) as n
FROM    Clothing;

CREATE INDEX IF NOT EXISTS term_document_assigner_index ON TermDocumentAssigner(document_id);
