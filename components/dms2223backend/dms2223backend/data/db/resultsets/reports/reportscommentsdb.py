""" 
Comments reports class module.
"""

from typing import List
from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm.session import Session  # type: ignore
from sqlalchemy.orm.exc import NoResultFound  # type: ignore
from dms2223backend.data.db.results.report.reportcommentdb import ReportComment
from dms2223backend.data.db.resultsets.commentsdb import Comments




class ReportsComments():
    """ Class responsible of table-level comment reports operations.
    """
    @staticmethod
    def create(session: Session, reason: str) -> ReportComment:
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


        new_report = ReportComment(session, reason)

        # TODO: no creo que con list_all valga
        if not new_report.cid in Comments.list_all():
            raise ValueError('No existe un comentario con ese identificador')
        
        session.add(new_report)
        session.commit()
        return new_report


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


