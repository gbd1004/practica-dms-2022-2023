"""
Reports class module.
"""
from sqlalchemy import Integer, Table, MetaData, Column, String, Enum # type: ignore
from sqlalchemy import DateTime, case, func # type: ignore
from dms2223backend.data.db.results.resultsbase import ResultBase
from dms2223backend.data.reportstatus import ReportStatus

class Report(ResultBase):
    """ Definition and storage of reports ORM records.
    """

    def __init__(self, eid:int, type:str, reason:str, status:ReportStatus, owner: str):
        """ Constructor method.

        Initializes a reports record.

        Args:
            - id (int) : A integer with the report's id.
            - eid (int) : A integer with the identifier of the answer or cuestion.
            - type (str) : A string with the type (answer, comment or question).
            - timestamp (datetime.timestamp) : The report's creation date.
            - reason (str) : A string with the report's reason.
            - status (Enum) : The report's status.
            - owner (str) : A string with the report's owner.
        """
        self.id: int
        self.eid: int = eid
        self.type: str = type
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
            'report',
            metadata,
            Column('id', Integer, primary_key=True),
            Column('eid', Integer, nullable=False),
            Column('type', String(24), primary_key=True),
            Column('status', Enum(ReportStatus),default=ReportStatus.PENDING.name,nullable=False),
            Column('reason', String(300), nullable=False),
            Column('timestamp', DateTime, nullable=False, default=func.now()),
            Column('owner', String(64), nullable=False)
        )

    __mapper_args__ = {
        "polymorphic_on":case(
            [
                (type == "reportans", "reportans"),
                (type == "reportcomm", "reportcomm"),
                (type == "reportque", "reportque")
            ]
         )
    }
