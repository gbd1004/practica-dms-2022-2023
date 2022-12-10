""" 
Quesssstion class module.
"""
import time
from datetime import datetime
from typing import Dict
from sqlalchemy import Table, MetaData, Column, String  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from dms2223backend.data.db.results.resultsbase import ResultBase
from dms2223backend.service.authservice import AuthService
from dms2223backend.data.db.results.answerdb import Answer
from dms2223backend.data.db.results.report.reportquestiondb import ReportQuestion




class Question(ResultBase):
    """ Definition and storage of question ORM records.
    """

    def __init__(self, title: str, body: str, hidden: bool):
        """ Constructor method.

        Initializes a question record.

        Args:
            - qid (int) : A integer with the question's identifier
            - title (str): A string with the question's title.
            - body (str) : A string with the question's body.
            - timestamp (datetime.timestamp) : The question's creation date.
            - owner (str) : A string with the question's owner.
            - hidden (bool) : A boolean for moderators to hide items.
        """
        self.qid: int
        self.title: str = title
        self.body: str = body
        self.timestamp: datetime.timestamp
        self.owner: str
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
            'question',
            metadata,
            Column('qid', int, primary_key=True, autoincrement=True),
            Column('title', String(64), nullable=False),
            Column('body', String(200), nullable=True),
            Column('timestamp', datetime.timestamp, nullable=False, default=time.time()),
            Column('owner', String(64), nullable=False, default=AuthService.get_user()),
            Column('hidden', bool, nullable=False, default=False)
        )

    @staticmethod
    def _mapping_properties() -> Dict:
        # Definimos la "relación" entre preguntas y respuestas
        return {
            'question_answer': relationship(Answer, backref='qid'),
            'question_report': relationship(ReportQuestion, backref='qid')
        }

