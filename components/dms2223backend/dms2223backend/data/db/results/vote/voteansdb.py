"""
Answer votes class module.
"""

from sqlalchemy import ForeignKey, Integer, Table, MetaData, Column, String  # type: ignore
from dms2223backend.data.db.results.resultsbase import ResultBase  # type: ignore

class VotesAns(ResultBase):
    """ Definition and storage of answer votes ORM records.
    """

    def __init__(self, aid:int, user:str):
        """ Constructor method.

        Initializes a vote record.

        Args:
            - id (int) : A integer with the identifier of the answer.
            - owner (str) : A string with the vete's owner.
        """
        self.aid: int = aid
        self.user: str = user

    @staticmethod
    def _table_definition(metadata: MetaData) -> Table:
        """ Gets the table definition.
        Args:
            - metadata (MetaData): The database schema metadata
                        (used to gather the entities' definitions and mapping)
        Returns:
            - Table: A `Table` object with the table definition.
        """
        return Table(
            'voteanswer',
            metadata,
            Column('aid', Integer, ForeignKey('answer.aid'), primary_key=True),
            Column('user', String(64), primary_key=True)
        )
