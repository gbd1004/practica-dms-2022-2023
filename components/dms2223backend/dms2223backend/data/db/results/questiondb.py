""" User class module.
"""
import time
from datetime import datetime
from typing import Dict
from flask import current_app
from sqlalchemy import Table, MetaData, Column, String  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from dms2223backend.data.db.results.resultsbase import ResultBase
from dms2223auth.dms2223auth.presentation.rest import server




class Question(ResultBase):
    """ Definition and storage of question ORM records.
    """

    def __init__(self,title: str, body: str):
        """ Constructor method.

        Initializes a question record.

        Args:
            - qid (int) : A integer with the question's identifier
            - title (str): A string with the question's title.
            - body (str) : A string with the question's body.
            - timestamp (datetime.timestamp) : The question's creation date.
            - owner (str) : A string with the question's owner.
        """
        self.qid: int
        self.title: str = title
        self.body: str = body
        self.timestamp: datetime.timestamp = time.time()
        self.owner: str = server.get_token_owner().value() # TODO: revisar si el token es correcto



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
            Column('timestamp', datetime.timestamp, nullable=False),
            Column('owner', String(64), nullable=False)
        )

    

