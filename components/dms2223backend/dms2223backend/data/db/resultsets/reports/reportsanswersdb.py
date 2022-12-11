""" 
Answer reports class module.
"""

from typing import List
from sqlalchemy.orm.session import Session  # type: ignore
from sqlalchemy.orm.exc import NoResultFound
from dms2223backend.data.db.results.report.reportanswerdb import ReportAnswer
from dms2223backend.data.db.resultsets.answersdb import Answers




class ReportsAnswer():
    """ Class responsible of table-level answer reports operations.
    """
    @staticmethod
    def create(session: Session, reason: str) -> ReportAnswer:
        """ Creates a new report record.

        Note:
            Any existing transaction will be committed.

        Args:
            - session (Session): The session object.
            - reason (str): The report's reason.

        Raises:
            - ValueError: If the reason is empty.
            - QuestionNotFound: If the referenced answer do not exists.

        Returns:
            - ReportAnswer: The created `Report` result.
        """

        if not reason:
            raise ValueError('Reason is a required value')

        new_report = ReportAnswer(session, reason)
        
        session.add(new_report)
        session.commit()
        return new_report

    @staticmethod
    def get_report(session: Session, arid:int) -> ReportAnswer:
        """Gets a particular report.

        Args:
            - session (Session): The session object.
            - arid (int): The report's id

        Returns:
            - Report: Expected `Report` register.
        """
        
        query = session.query(ReportAnswer).where(ReportAnswer.id == arid)
        return query

    @staticmethod
    def list_all(session: Session) -> List[ReportAnswer]:
        """Lists every answer report.

        Args:
            - session (Session): The session object.

        Returns:
            - List[ReportAnswer]: A list of `Reports` registers.
        """
        
        query = session.query(ReportAnswer)
        return query.all()


