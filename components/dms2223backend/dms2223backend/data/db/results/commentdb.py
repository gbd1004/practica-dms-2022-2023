""" 
Comment class module.
"""
import time
from datetime import datetime
from typing import Dict
from sqlalchemy.orm.session import Session  # type: ignore
from sqlalchemy import ForeignKey, Table, MetaData, Column, String, Enum  # type: ignore
from sqlalchemy.orm import relationship
from dms2223backend.data.db.results.report.reportcommentdb import ReportComment  # type: ignore
from dms2223backend.data.db.results.resultsbase import ResultBase
from dms2223backend.service.authservice import AuthService
from dms2223backend.data.db.results.vote.votescommdb import VotesComm
from dms2223backend.data.sentiment import Sentiment




class Comment(ResultBase):
    """ Definition and storage of comment ORM records.
    """

    def __init__(self, aid: int, body: str, sentiment: Sentiment, auth_service: AuthService):
        """ Constructor method.

        Initializes a comment record.

        Args:
            - id (int) : A integer with the comment's identifier.
            - aid (int) : A integer with the related answer's identifier.
            - timestamp (datetime.timestamp) : The comment's creation date.
            - body (str) : A string with the comment's body.
            - owner (str) : A string with the comment's owner.
            - sentiment (enum): A enumerated type with the comment's sentiment.
        """
        self.id: int
        self.aid: int = aid
        self.body: str = body
        self.timestamp: datetime.timestamp
        self.owner: str 
        self.sentiment: Sentiment = sentiment
        self.votes: int






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
            'coment',
            metadata,
            Column('id', int, primary_key=True, autoincrement=True),
            Column('aid', int, ForeignKey('answer.aid'), nullable=False), 
            Column('body', String(200), nullable=True),
            Column('timestamp', datetime.timestamp, nullable=False, default=time.time()),
            Column('owner', String(64), nullable=False, default=AuthService.get_user()),
            Column('sentiment', Enum(Sentiment), nullable=True), 
            Column('votes', int, nullable=True,onupdate=VotesComm.num_votes(Session,Comment.id))
        )

    @staticmethod
    def _mapping_properties() -> Dict:
        # Definimos la "relación" entre comentarios y votos
        return {
            'comment_vote': relationship(VotesComm, backref='id'),
            'comment_report': relationship(ReportComment, backref='id')
        }


    

        



    

