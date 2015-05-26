
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS Term 
(
    term_id         INTEGER PRIMARY KEY,
    name            TEXT UNIQUE NOT NULL,
    datatype        TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS TermDocumentAssigner 
(
    term_id         INTEGER NOT NULL,
    document_id     INTEGER NOT NULL,

    PRIMARY KEY(term_id, document_id),

    FOREIGN KEY(term_id) REFERENCES Term(term_id),
    FOREIGN KEY(document_id) REFERENCES Clothing(document_id)
);

-- total number of documents
CREATE VIEW IF NOT EXISTS N AS
SELECT  (SELECT COUNT(*) FROM Clothing) AS document_count,
        (SELECT COUNT(*) FROM Term) AS term_count
;

CREATE INDEX IF NOT EXISTS term_document_assigner_index ON TermDocumentAssigner(document_id);
