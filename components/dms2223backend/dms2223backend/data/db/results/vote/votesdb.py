"""
Answer votes class module.
"""

from sqlalchemy import Table, MetaData, Column, String, case  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from dms2223backend.data.db.results.resultsbase import ResultBase


class Votes(ResultBase):
    """ Definition and storage of votes ORM records.
    """

    def __init__(self, id:int, type:str, user:str):
        """ Constructor method.

        Initializes a vote record.

        Args:
            - id (int) : A integer with the identifier of the answer or comment.
            - type (str) : A string with the type (answer or comment).
            - owner (str) : A string with the vete's owner.
        """
        self.id: int = id
        self.type: str = type
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
            'votes',
            metadata,
            Column('id', int, primary_key=True),
            Column('type', String(24), primary_key=True),
            Column('user', String(64), nullable=False)
        )

    __mapper_args__ = {
        #'polymorphic_identity':'votes',
        "polymorphic_on":case(
            [
                (type == "voteanswer", "voteanswer"),
                (type == "votecomment", "votecomment")
            ]
         )
    }






        



    

