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





class Votes(ResultBase):
    """ Definition and storage of answer ORM records.
    """

    def __init__(self, id:int, type:str, user:str):
        """ Constructor method.

        Initializes a vote record.

        Args:
            - id (int) : A integer with the identifier of the answer or cuestion.
            - type (str) : A string with the type (answer or comment).
            - owner (str) : A string with the vete's owner.
        """
        self.id: int = id
        self.type: str = type
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
            'vote',
            metadata,
            Column('id', int, primary_key=True),
            Column('type', String(24), primary_key=True),
            Column('user', String(64), nullable=False)
        )

    # Método con el que posteriormente se puede actualizar el número de votos 
    # Se empleará cada vez que se cree un voto -> IMPORTANTE
    @staticmethod
    def num_votes(session: Session, id:int, type:str) -> int:
        num = session.query(Votes).filter(Votes.type == type, Votes.id == id)
        return num.count()



    #TODO: ¿ES NECESARIO? PREGUNTAR
    '''
    @staticmethod
    def _mapping_properties() -> Dict:
        return {
                'question': relationship(Question, backref='answer')
            }
    '''

        



    

