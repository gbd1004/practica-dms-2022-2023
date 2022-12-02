""" 
Answer class module.
"""
import time
from datetime import datetime
from typing import Dict
from sqlalchemy.orm.session import Session  # type: ignore
from sqlalchemy import ForeignKey, Table, MetaData, Column, String  # type: ignore
from sqlalchemy.orm import relationship
from dms2223backend.data.db.results.report.reportanswerdb import ReportAnswer  # type: ignore
from dms2223backend.data.db.results.resultsbase import ResultBase
from dms2223backend.data.db.results.vote.votesansdb import VotesAns
from dms2223backend.data.db.results.commentdb import Comment
from dms2223backend.service.authservice import AuthService




class Answer(ResultBase):
    """ Definition and storage of answer ORM records.
    """

    def __init__(self, qid: int, body: str):
        """ Constructor method.

        Initializes a answer record.

        Args:
            - aid (int) : A integer with the answer's identifier.
            - qid (int) : A integer with the related question's identifier.
            - timestamp (datetime.timestamp) : The answer's creation date.
            - body (str) : A string with the answer's body.
            - owner (str) : A string with the answer's owner.
            - votes (int) : A integer with the number of votes.
        """
        self.aid: int
        self.qid: int = qid
        self.body: str = body
        self.timestamp: datetime.timestamp
        self.owner: str
        self.votes: int = 0





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
            'answer',
            metadata,
            Column('aid', int, primary_key=True, autoincrement=True),
            Column('qid', int, ForeignKey('question.qid'), nullable=False), 
            Column('body', String(200), nullable=True),
            Column('timestamp', datetime.timestamp, nullable=False, default=time.time()),
            Column('owner', String(64), nullable=False, default=AuthService.get_user()),
            Column('votes', int, nullable=True, onupdate=VotesAns.num_votes(Session,Answer.aid))
        )
    


    @staticmethod
    def _mapping_properties() -> Dict:
        # Definimos la "relación" entre respuestas y comentarios
        # Definimos la "relación" entre respuestas y votos
        return {
            'answer_comment': relationship(Comment, backref='aid'),
            'answer_votes': relationship(VotesAns, backref='aid'),
            'answer_reports': relationship(ReportAnswer, backref='aid')
        }

    

        



    

