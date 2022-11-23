""" User class module.
"""
import time
from datetime import datetime
from typing import Dict
from flask import current_app
from sqlalchemy.orm.session import Session  # type: ignore
from sqlalchemy import ForeignKey, Table, MetaData, Column, String  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from dms2223backend.data.db.results.resultsbase import ResultBase
from dms2223auth.dms2223auth.presentation.rest import server
from dms2223backend.data.db.results.answerdb import Answer
from dms2223backend.presentation import answers
from dms2223backend.data.db.results.votesdb import Votes




class Comment(ResultBase):
    """ Definition and storage of comment ORM records.
    """

    def __init__(self, session:Session, body: str, sentiment: enumerate):
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
        self.aid: int = answers.get_aid() #TODO: hacer el método en el endpiont
        self.body: str = body
        self.timestamp: datetime.timestamp = time.time()
        self.owner: str = server.get_token_owner().value() # TODO: revisar si el token es correcto
        self.sentiment: enumerate = sentiment
        self.votes: int = Votes.num_votes(session,self.id,'comment') # TODO: Ver si efectivamente se actualiza dinámicamente 






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
            Column('aid', int, ForeignKey(Answer.aid), nullable=False), 
            Column('body', String(200), nullable=True),
            Column('timestamp', datetime.timestamp, nullable=False),
            Column('owner', String(64), nullable=False),
            Column('sentiment', enumerate, nullable=False),
            Column('votes', int, nullable=True) #TODO: ver como conectar la tabla
        )
    

    
        #TODO: ¿ES NECESARIO? Ya tenemos FK ->Ya tenemos FK -> PREGUNTAR
        """ 
        @staticmethod
        def _mapping_properties() -> Dict:

            return {
                'answer': relationship(Answer, backref='comment')
            }
        """
        



    

