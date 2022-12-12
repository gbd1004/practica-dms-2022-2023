"""
Comments votes class module.
"""

from sqlalchemy.orm.session import Session  # type: ignore
from sqlalchemy import ForeignKey, Integer,Table, MetaData, Column, String  # type: ignore
from dms2223backend.data.db.results.vote.votedb import Votes




class VotesComm(Votes):
    """ Definition and storage of comments votes ORM records.
    """

    def __init__(self, cid:int, user:str):
        """ Constructor method.

        Initializes a vote record.

        Args:
            - id (int) : A integer with the identifier of the comment
            - owner (str) : A string with the vote's owner.
        """
        self.cid: int = cid
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
            'votecomment',
            metadata,
            Column('id', Integer,primary_key=True, autoincrement=True),
            Column('cid', Integer, ForeignKey('comment.id')),
            Column('user', String(64), nullable=False)
        )



    # El discriminante "type" se decanta por "comment"
    # __mapper_args__ = {
    #     'polymorphic_identity': 'votecomment', 
    # }


    

        



    

