""" 
Questions reports class module.
"""

from typing import List
from sqlalchemy.orm.session import Session  # type: ignore
from sqlalchemy.orm.exc import NoResultFound  # type: ignore
from dms2223backend.data.db.results.report.reportquestiondb import ReportQuestion
from dms2223backend.data.db.resultsets.questionsdb import Questions




class ReportsQuestions():
    """ Class responsible of table-level question reports operations.
    """
    @staticmethod
    def create(session: Session, reason: str) -> ReportQuestion:
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
            - ReportQuestion: The created `Report` result.
        """

        if not reason:
            raise ValueError('Reason is a required value')


        new_report = ReportQuestion(session, reason)

        # TODO: no creo que con list_all valga
        if not new_report.qid in Questions.list_all():
            raise ValueError('No existe una pregunta con ese identificador')
        
        session.add(new_report)
        session.commit()
        return new_report


    @staticmethod
    def list_all(session: Session) -> List[ReportQuestion]:
        """Lists every comment report.

        Args:
            - session (Session): The session object.

        Returns:
            - List[ReportQuestion]: A list of `Reports` registers.
        """
        
        query = session.query(ReportQuestion)
        return query.all()

