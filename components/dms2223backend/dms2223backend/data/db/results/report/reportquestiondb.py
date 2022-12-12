"""
Question reports class module.
"""

import time
from datetime import datetime
from sqlalchemy import ForeignKey, Integer, Table # type: ignore
from sqlalchemy import MetaData, Column, String, Enum, DateTime, func # type: ignore
from sqlalchemy.orm import relationship # type: ignore
from dms2223backend.data.db.results.report.reportdb import Report
from dms2223backend.data.reportstatus import ReportStatus

class ReportQuestion(Report):
    """ Definition and storage of reports ORM records.
    """

    def __init__(self, qid:int, reason:str, status:ReportStatus, owner: str):
        """ Constructor method.

        Initializes a reports record.

        Args:
            - id (int) : A integer with the report's id.
            - qid (int) : A integer with the identifier of the question.
            - timestamp (datetime.timestamp) : The report's creation date.
            - reason (str) : A string with the report's reason.
            - status (Enum) : The report's status.
            - owner (str) : A string with the report's owner.
        """
        self.id: int
        self.qid: int = qid
        self.reason: str = reason
        self.status: ReportStatus = status
        self.owner: str = owner

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
            'reportquest',
            metadata,
            Column('id', Integer, primary_key=True),
            Column('qid', Integer, ForeignKey('question.qid'), nullable=False),
            Column('status', Enum(ReportStatus), default=ReportStatus.PENDING, nullable=False),
            Column('reason', String(300), nullable=False),
            Column('timestamp', DateTime, nullable=False, default=func.now()),
            Column('owner', String(64), nullable=False)
        )

    # El discriminante "type" se decanta por "comment"
    __mapper_args__ = {
        'polymorphic_identity': 'reportque', 
    }
