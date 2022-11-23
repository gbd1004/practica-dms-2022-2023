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
from dms2223backend.data.db.results.questiondb import Question
from dms2223backend.presentation import questionsdb
from dms2223backend.data.db.results.votesdb import Votes




class Answer(ResultBase):
    """ Definition and storage of answer ORM records.
    """

    def __init__(self, session:Session, body: str):
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
        self.qid: int = questionsdb.get_qid() #TODO: hacer el método en el endpiont
        self.body: str = body
        self.timestamp: datetime.timestamp = time.time()
        self.owner: str = server.get_token_owner().value() # TODO: revisar si el token es correcto
        self.votes: int = Votes.num_votes(session,self.aid,'answer') # TODO: Ver si efectivamente se actualiza dinámicamente





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
            Column('qid', int, ForeignKey(Question.qid), nullable=False), 
            Column('body', String(200), nullable=True),
            Column('timestamp', datetime.timestamp, nullable=False),
            Column('owner', String(64), nullable=False),
            Column('votes', int, nullable=True) #TODO: ver como conectar la tabla
        )
    


        #TODO: ¿ES NECESARIO? Ya tenemos FK -> PREGUNTAR
        """ 
        @staticmethod
        def _mapping_properties() -> Dict:

            return {
                'question': relationship(Question, backref='answer')
            }
        """
        



    

