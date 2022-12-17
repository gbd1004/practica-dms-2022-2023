"""
Answer class module.
"""

from typing import Dict
from sqlalchemy import Table, MetaData, Column, String, func # type: ignore
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer # type: ignore
from sqlalchemy.orm import relationship # type: ignore
from dms2223backend.data.db.results.report.reportanswerdb import ReportAnswer  # type: ignore
from dms2223backend.data.db.results.resultsbase import ResultBase
from dms2223backend.data.db.results.vote.voteansdb import VotesAns
from dms2223backend.data.db.results.commentdb import Comment

class Answer(ResultBase):
    """ Definition and storage of answer ORM records.
    """

    def __init__(self, qid: int, body: str, hidden: bool, owner: str):
        """ Constructor method.

        Initializes a answer record.

        Args:
            - aid (int) : A integer with the answer's identifier.
            - qid (int) : A integer with the related question's identifier.
            - timestamp (datetime.timestamp) : The answer's creation date.
            - body (str) : A string with the answer's body.
            - owner (str) : A string with the answer's owner.
            - hidden (bool) : A boolean for moderators to hide items.
        """
        self.aid: int
        self.qid: int = qid
        self.body: str = body
        self.owner: str = owner
        self.hidden: bool = hidden
        self.timestamp: DateTime

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
            Column('aid', Integer, primary_key=True, autoincrement=True),
            Column('qid', Integer, ForeignKey('question.qid'), nullable=False),
            Column('body', String(200), nullable=True),
            Column('timestamp', DateTime, nullable=False, default=func.now()),
            Column('owner', String(64), nullable=False),
            Column('hidden', Boolean, nullable=False, default=False)
        )

    @staticmethod
    def _mapping_properties() -> Dict:
        # Definimos la "relación" entre respuestas y comentarios
        # Definimos la "relación" entre respuestas y votos
        return {
            'answer_comment': relationship(Comment, backref='answer'),
            'answer_votes': relationship(VotesAns, backref='answer'),
            'answer_reports': relationship(ReportAnswer, backref='answer')
        }

    
