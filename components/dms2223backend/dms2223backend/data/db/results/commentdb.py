""" 
Comment class module.
"""
import time
from datetime import datetime
from typing import Dict
from sqlalchemy.orm.session import Session  # type: ignore
from sqlalchemy import ForeignKey, Table, MetaData, Column, String, Enum, func  # type: ignore
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Table, MetaData, Column, String
from sqlalchemy.orm import relationship
from dms2223backend.data.db.results.report.reportcommentdb import ReportComment  # type: ignore
from dms2223backend.data.db.results.resultsbase import ResultBase
from dms2223backend.data.db.results.vote.votecommdb import VotesComm
from dms2223backend.data.sentiment import Sentiment




class Comment(ResultBase):
    """ Definition and storage of comment ORM records.
    """

    def __init__(self, aid: int, body: str, sentiment: Sentiment, hidden:bool, owner: str):
        """ Constructor method.

        Initializes a comment record.

        Args:
            - id (int) : A integer with the comment's identifier.
            - aid (int) : A integer with the related answer's identifier.
            - timestamp (datetime.timestamp) : The comment's creation date.
            - body (str) : A string with the comment's body.
            - owner (str) : A string with the comment's owner.
            - sentiment (enum): A enumerated type with the comment's sentiment.
            - hidden (bool) : A boolean for moderators to hide items
        """
        self.id: int
        self.aid: int = aid
        self.body: str = body
        self.owner: str = owner
        self.sentiment: Sentiment = sentiment
        self.hidden: bool = hidden

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
            'comment',
            metadata,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('aid', Integer, ForeignKey('answer.aid'), nullable=False), 
            Column('body', String(200), nullable=True),
            Column('timestamp', DateTime, nullable=False, default=func.now()),
            Column('owner', String(64), nullable=False),
            Column('sentiment', Enum(Sentiment), nullable=True), 
            Column('hidden', Boolean, nullable=False, default=False)
        )

    @staticmethod
    def _mapping_properties() -> Dict:
        # Definimos la "relación" entre comentarios y votos
        return {
            'comment_vote': relationship(VotesComm, backref='comment'),
            'comment_report': relationship(ReportComment, backref='comment')
        }

    # Método con el que posteriormente se puede actualizar el número de votos 
    def get_num_votes(self, session: Session) -> int:
        num_votes = session.query(VotesComm).filter(VotesComm.id == self.id)
        return num_votes.count()


    

        



    

