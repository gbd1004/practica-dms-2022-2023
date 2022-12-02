"""
Comments votes class module.
"""

from sqlalchemy.orm.session import Session  # type: ignore
from sqlalchemy import ForeignKey,Table, MetaData, Column, String  # type: ignore
from dms2223backend.data.db.results.vote.votesdb import Votes




class VotesComm(Votes):
    """ Definition and storage of comments votes ORM records.
    """

    def __init__(self, id:int, type:str, user:str):
        """ Constructor method.

        Initializes a vote record.

        Args:
            - id (int) : A integer with the identifier of the comment
            - owner (str) : A string with the vote's owner.
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
            'votecomment',
            metadata,
            Column('id', int, ForeignKey('comment.id'),primary_key=True),
            Column('user', String(64), nullable=False)
        )

    # Método con el que posteriormente se puede actualizar el número de votos 
    # Se empleará cada vez que se cree un voto -> IMPORTANTE
    @staticmethod
    def num_votes(session: Session, id:int) -> int:
        num = session.query(Votes).filter(Votes.id == id)
        return num.count()


    # El discriminante "type" se decanta por "comment"
    __mapper_args__ = {
        'polymorphic_identity': 'votecomment', 
    }


    

        



    
