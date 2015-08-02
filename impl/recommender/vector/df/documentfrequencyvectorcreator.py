

from ..abstractvector import VectorCreator
from . import DocumentFrequencyVector

class DocumentFrequencyVectorCreator(VectorCreator):
    """Creates document-frequency vectors

    Inherits from :class:`recommender.vector.abstractvector.VectorCreator`

    :parameter sqlite3_connection: connection to a database build with :class:`recommender.vector.vectortablecreator.VectorTableCreator`
    :type sqlite3_connection: sqlite3.Connection
    :raises: TypeError
    """
    
    def __init__(self, db_connection_str):
        super(DocumentFrequencyVectorCreator, self).__init__(db_connection_str)
        self._create_document_frequency_view()
        pass

    def _create_document_frequency_view(self):
        """A preparation for creating DocumentFrequencyVectors a View for calculating the documentfrequency is necessary.

        Will be called by :func:`__init__`.
        """
        with self._get_db_connection() as conn:
            c = conn.cursor()
            c.execute(
                '''
                CREATE VIEW IF NOT EXISTS [DocumentFrequency] AS
                    SELECT
                        [t].[term_id]
                        , [t].[name]
                        , CASE WHEN   [a].[count] IS NULL
                            THEN    0
                            ELSE    [a].[count]
                        END AS value
                    FROM
                        [Term] as [t]
                        LEFT OUTER JOIN
                        (
                            SELECT      [term_id], SUM([count]) AS [count]
                            FROM        [TermDocumentAssigner]
                            GROUP BY    [term_id]
                        ) AS [a]
                            ON [t].[term_id] = [a].[term_id]
                    ORDER BY
                        [t].[term_id]
                ;
                ''')
        pass

    def _create_vector(self, document_id=None):
        """Creates a vector containing the documentfrequency of all terms.

        Will be called by :func:`recommender.vector.abstractvector.VectorCreatorFabric.get_vector`.

        :parameter document_id: Will be ignored (due to compatibility with the ancestor the parameter is available)
        :type document_id: None
        """
        vector = DocumentFrequencyVector()
        
        values = self._get_vector_values_from_db()
        for value in [] if values is None else values:
            vector.add_to_vector(value)
        return vector

    def _get_vector_values_from_db(self):
        """Get the documentfrequency values form the db

        :returns: list(int) -- a list of occurences of the different terms
        """
        with self._get_db_connection() as conn:
            c = conn.cursor()
            c.execute(
                '''
                SELECT
                    [term_id]
                    , [name]
                    , [value]
                FROM
                    [DocumentFrequency]
                ;
                ''')
            vector_values = []
            for result in c.fetchall():
                vector_values.append((result[0], result[1], result[2]))
                pass
            return None if not vector_values else vector_values
   

