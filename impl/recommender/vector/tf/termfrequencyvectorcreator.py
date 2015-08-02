
import sqlite3

from ..abstractvector import VectorCreator
from . import TermFrequencyVector

class TermFrequencyVectorCreator(VectorCreator):
    """Creates term-frequency vectors

    Inherits from :class:`recommender.vector.abstractvector.VectorCreatorFabric`

    :parameter sqlite3_connection: connection to a database build with :class:`recommender.vector.vectortablecreator.VectorTableCreator`
    :type sqlite3_connection: sqlite3.Connection
    :raises: TypeError
    """

    def __init__(self, db_connection_str):
        super(TermFrequencyVectorCreator, self).__init__(db_connection_str)
        pass

    def _create_vector(self, document_id):
        """Creates a vector containing the termfrequency for a given document.

        Will be called by :func:`recommender.vector.abstractvector.AbstractVectorFabric.get_vector`
        """
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            if not self._has_document(cursor, document_id):
                return None
            return self._create_vector_no_check(cursor, document_id)

    def _create_vector_no_check(self, cursor, document_id):
        """Create a vector without further checks for existance of a document

        :param document_id: the document_id that will be checked for existance
        :type document_id: int
        :returns: :class:`recommendervector.termfrequency.TermFrequencyVector` -- a vector containing all terms, their description plus the termfrequency
        """
        vector = TermFrequencyVector()
        values = self._get_vector_values_from_db(cursor, document_id)

        for value in [] if values is None else values:
            vector.add_to_vector(value)
            pass
        return vector


    def _has_document(self, c, document_id):
        """

        :param document_id: the document_id that will be checked for existance
        :type document_id: int
        :returns: bool -- indicating whether there is a document with the given document_id or not
        """
        c.execute(
            '''
            SELECT
                document_id
            FROM
                Document
            WHERE
                document_id = :document_id
            ''', {'document_id': document_id}
        )
        return c.fetchone() is not None

    def _get_vector_values_from_db(self, c, document_id):
        """Retrieve the values stored in the database for a given document_id

        :param document_id: the document_id for which the values will be retrieved
        :type document_id: int
        :returns: list(values) -- list of termfrequency-values
        """
        c.execute(
            '''
            SELECT
                t.term_id
                , t.name
                , CASE WHEN   a.document_id IS NULL
                    THEN    0
                    ELSE    a.count
                END AS value
            FROM
                Term AS t
                LEFT OUTER JOIN
                (
                    SELECT
                        term_id
                        , document_id
                        , count
                    FROM
                        TermDocumentAssigner
                    WHERE
                        document_id = :document_id
                ) AS a ON t.term_id = a.term_id
            ORDER BY    t.term_id
            ;
            ''', {'document_id': document_id})
        vector_values = []
        for result in c.fetchall():
            vector_values.append((result[0], result[1], result[2]))
            pass
        return None if not vector_values else vector_values
