""" 
Answer votes class module.
"""

from sqlalchemy import ForeignKey, Table, MetaData, Column, String  # type: ignore
from dms2223backend.data.db.results.vote.votedb import Votes




class VotesAns(Votes):
    """ Definition and storage of answer votes ORM records.
    """

    def __init__(self, id:int, user:str):
        """ Constructor method.

        Initializes a vote record.

        Args:
            - id (int) : A integer with the identifier of the answer.
            - owner (str) : A string with the vete's owner.
        """
        self.id: int = id
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
            Column('id', int, ForeignKey('answer.aid'), primary_key=True),
            Column('user', String(64), nullable=False)
        )


    # El discriminante "type" se decanta por "answer"
    __mapper_args__ = {
        'polymorphic_identity': 'voteanswer', 
    }

    

        



    
