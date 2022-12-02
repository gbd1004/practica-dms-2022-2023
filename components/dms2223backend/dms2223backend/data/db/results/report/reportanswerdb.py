"""
Answer reports class module.
"""

import time
from datetime import datetime
from sqlalchemy.orm.session import Session  # type: ignore
from sqlalchemy import ForeignKey, Table, MetaData, Column, String, Enum  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from dms2223backend.data.db.results.report.reportdb import Report
from dms2223backend.data.reportstatus import ReportStatus
from dms2223backend.service.authservice import AuthService




class ReportAnswer(Report):
    """ Definition and storage of reports ORM records.
    """

    def __init__(self, aid:int, type:str, reason:str, status:ReportStatus):
        """ Constructor method.

        Initializes a reports record.

        Args:
            - id (int) : A integer with the report's id.
            - aid (int) : A integer with the identifier of the answer
            - timestamp (datetime.timestamp) : The report's creation date.
            - reason (str) : A string with the report's reason.
            - status (Enum) : The report's status.
            - owner (str) : A string with the report's owner.
        """
        self.id: int
        self.aid: int = aid
        self.timestamp: datetime.timestamp
        self.reason: str = reason
        self.status: ReportStatus = status
        self.owner: str


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
            'reportans',
            metadata,
            Column('id', int, primary_key=True),
            Column('aid', int, ForeignKey('answer.aid'), nulleable=False),
            Column('status', Enum(ReportStatus), default=ReportStatus.PENDING.name, nullable=False),#TODO: on-update?
            Column('reason', String(300), nullable=False),
            Column('timestamp', datetime.timestamp, nullable=False, default=time.time()),
            Column('owner', String(64), nullable=False, default=AuthService.get_user()) # TODO: Revisar en servicios
        )


    # El discriminante "type" se decanta por "answer"
    __mapper_args__ = {
        'polymorphic_identity': 'reportans', 
    }


    

        



    
