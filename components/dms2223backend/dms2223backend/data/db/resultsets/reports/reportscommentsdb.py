"""
Comments reports class module.
"""

from typing import List
from sqlalchemy.orm.session import Session  # type: ignore
from dms2223backend.data.db.results.report.reportcommentdb import ReportComment
from dms2223backend.data.reportstatus import ReportStatus

class ReportsComments():
    """ Class responsible of table-level comment reports operations.
    """
    @staticmethod
    def create(session: Session, cid:int, reason: str, owner: str) -> ReportComment:
        """ Creates a new report record.

        Note:
            Any existing transaction will be committed.

        Args:
            - session (Session): The session object.
            - reason (str): The report's reason.

        Raises:
            - ValueError: If the reason is empty.
            - QuestionNotFound: If the referenced comment do not exists.

        Returns:
            - ReportComment: The created `Report` result.
        """

        if not reason:
            raise ValueError('Reason is a required value')

        new_report = ReportComment(cid, reason, ReportStatus.PENDING, owner)

        session.add(new_report)
        session.commit()
        return new_report

    @staticmethod
    def get_report(session: Session, crid:int) -> ReportComment:
        """Gets a particular report.

        Args:
            - session (Session): The session object.
            - crid (int): The report's id

        Returns:
            - Report: Expected `Report` register.
        """

        query = session.query(ReportComment).where(ReportComment.id == crid)
        return query.first()

    @staticmethod
    def list_all(session: Session) -> List[ReportComment]:
        """Lists every comment report.

        Args:
            - session (Session): The session object.

        Returns:
            - List[ReportComment]: A list of `Reports` registers.
        """

        query = session.query(ReportComment)
        return query.all()
