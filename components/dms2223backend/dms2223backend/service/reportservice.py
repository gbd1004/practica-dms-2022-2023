"""
ReportServices class module.
"""

from typing import List
from sqlalchemy.orm.session import Session # type: ignore
from dms2223backend.data.db.results.report.reportanswerdb import ReportAnswer
from dms2223backend.data.db.results.report.reportcommentdb import ReportComment
from dms2223backend.data.db.results.report.reportdb import Report
from dms2223backend.data.db.results.report.reportquestiondb import ReportQuestion
from dms2223backend.data.db.resultsets.reports.reportsanswersdb import ReportsAnswer
from dms2223backend.data.db.resultsets.reports.reportscommentsdb import ReportsComments
from dms2223backend.data.db.resultsets.reports.reportsquestionsdb import ReportsQuestions
from dms2223backend.data.db.schema import Schema
from dms2223backend.data.reportstatus import ReportStatus
from dms2223backend.service.answerservice import AnswerServices
from dms2223backend.service.commentservice import CommentServices
from dms2223backend.service.questionservice import QuestionServices


class ReportServices():
    """
    Monostate class that provides high-level services to handle Reports' use cases.
    """

    @staticmethod
    def get_reports_questions(schema: Schema) -> List[dict]:
        """Lists the existing reports.

        Args:
            - schema (Schema): A database handler where the reports are mapped into.

        Returns:
            - List[dict]: A list of dictionaries with the reports' data.
        """
        out: List = []
        session: Session = schema.new_session()
        reports: List[ReportQuestion] = ReportsQuestions.list_all(session)
        for report in reports:
            out.append({
                'qrid': report.id,
                'qid': report.qid,
                'timestamp': report.timestamp,
                'reason' : report.reason,
                'status': report.status.name,
                'owner': {'username': report.owner}
            })
        schema.remove_session()
        return out

    @staticmethod
    def get_reports_answers(schema: Schema) -> List[dict]:
        """Lists the existing reports.

        Args:
            - schema (Schema): A database handler where the reports are mapped into.

        Returns:
            - List[dict]: A list of dictionaries with the reports' data.
        """
        out: List = []
        session: Session = schema.new_session()
        reports: List[ReportAnswer] = ReportsAnswer.list_all(session)
        for report in reports:
            out.append({
                'arid': report.id,
                'aid': report.aid,
                'timestamp': report.timestamp,
                'reason' : report.reason,
                'status': report.status.name,
                'owner': {'username': report.owner}
            })
        schema.remove_session()
        return out

    @staticmethod
    def get_reports_comments(schema: Schema) -> List[dict]:
        """Lists the existing reports.

        Args:
            - schema (Schema): A database handler where the reports are mapped into.

        Returns:
            - List[dict]: A list of dictionaries with the reports' data.
        """
        out: List = []
        session: Session = schema.new_session()
        reports: List[ReportComment] = ReportsComments.list_all(session)
        for report in reports:
            out.append({
                'crid': report.id,
                'cid': report.cid,
                'timestamp': report.timestamp,
                'reason' : report.reason,
                'status': report.status.name,
                'owner': {'username': report.owner}
            })
        schema.remove_session()
        return out

    @staticmethod
    def get_report_question(schema: Schema, qrid:int) -> dict:
        """Gets an specific report

        Args:
            - schema (Schema): A database handler where the reports are mapped into.
            - qrid (int): The report's id.

        Returns:
            - dict: A dictionary with the report's data.
        """
        session: Session = schema.new_session()
        report: ReportQuestion = ReportsQuestions.get_report(session, qrid)
        out = {
            'qrid': report.id,
            'qid': report.qid,
            'timestamp': report.timestamp,
            'reason' : report.reason,
            'status': report.status.name,
            'owner': {'username': report.owner}
        }
        schema.remove_session()
        return out

    @staticmethod
    def get_report_answer(schema: Schema, arid:int) -> dict:
        """Gets an specific report

        Args:
            - schema (Schema): A database handler where the reports are mapped into.
            - arid (int): The report's id.

        Returns:
            - dict: A dictionary with the report's data.
        """
        session: Session = schema.new_session()
        report: ReportAnswer = ReportsAnswer.get_report(session, arid)
        out = {
            'arid': report.id,
            'aid': report.aid,
            'timestamp': report.timestamp,
            'reason' : report.reason,
            'status': report.status.name,
            'owner': {'username': report.owner}
        }
        schema.remove_session()
        return out

    @staticmethod
    def get_report_comment(schema: Schema, crid:int) -> dict:
        """Gets an specific report

        Args:
            - schema (Schema): A database handler where the reports are mapped into.
            - crid (int): The report's id.

        Returns:
            - dict: A dictionary with the report's data.
        """
        session: Session = schema.new_session()
        report: ReportComment = ReportsComments.get_report(session, crid)
        out = {
            'crid': report.id,
            'cid': report.cid,
            'timestamp': report.timestamp,
            'reason' : report.reason,
            'status': report.status.name,
            'owner': {'username': report.owner}
        }
        schema.remove_session()
        return out

    @staticmethod
    def set_question_report_status(schema: Schema, qrid: int, status: str):
        """Changes the status of the report

        Args:
            - qrid (int): The report's id.
            - schema (Schema): A database handler where the reports are mapped into.
        """
        session: Session = schema.new_session()

        report: ReportQuestion = ReportsQuestions.get_report(session, qrid)

        report.status = ReportStatus[status]
        if status == 'ACCEPTED':
            QuestionServices.hide_question(schema, report.qid)

        # Actualizamos el reporte
        session.add(report)
        session.commit()

        schema.remove_session()

    @staticmethod
    def set_answer_report_status(schema: Schema, arid: int, status: str):
        """Changes the status of the report

        Args:
            - arid (int): The report's id.
            - schema (Schema): A database handler where the reports are mapped into.
        """
        session: Session = schema.new_session()

        report: ReportAnswer = ReportsAnswer.get_report(session, arid)

        report.status = ReportStatus[status]
        if status == 'ACCEPTED':
            AnswerServices.hide_answer(schema, report.aid)

        # Actualizamos el reporte
        session.add(report)
        session.commit()

        schema.remove_session()

    @staticmethod
    def set_comment_report_status(schema: Schema, crid: int, status: str):
        """Changes the status of the report

        Args:
            - crid (int): The report's id.
            - schema (Schema): A database handler where the reports are mapped into.
        """
        session: Session = schema.new_session()

        report: ReportComment = ReportsComments.get_report(session, crid)

        report.status = ReportStatus[status]
        if status == 'ACCEPTED':
            CommentServices.hide_comment(schema, report.id)

        # Actualizamos el reporte
        session.add(report)
        session.commit()

        schema.remove_session()


    @staticmethod
    def new_question_report(schema: Schema, qid:int, reason: str, owner: str) -> dict:
        """Creates a new report.

        Args:
            - reason (str): The report's reason.
            - schema (Schema): A database handler where the reports are mapped into.

        Returns:
            - dict: A dictionary with the new report's data.
        """

        session: Session = schema.new_session()
        out = {}
        try:
            new_report: ReportQuestion = ReportsQuestions.create(session, qid, reason, owner)
            out = {
                'qrid': new_report.id,
                'qid': new_report.qid,
                'timestamp': new_report.timestamp,
                'reason' : new_report.reason,
                'status': new_report.status.name,
                'owner': {'username': new_report.owner}
            }

        except Exception as ex:
            raise ex
        finally:
            schema.remove_session()
        return out

    @staticmethod
    def new_answer_report(schema: Schema, aid: int, reason: str, owner: str) -> dict:
        """Creates a new report.

        Args:
            - reason (str): The report's reason.
            - schema (Schema): A database handler where the reports are mapped into.
        Returns:
            - dict: A dictionary with the new report's data.
        """

        session: Session = schema.new_session()
        out = {}
        try:
            new_report: ReportAnswer = ReportsAnswer.create(session, aid, reason, owner)
            out = {
                'arid': new_report.id,
                'aid': new_report.aid,
                'timestamp': new_report.timestamp,
                'reason' : new_report.reason,
                'status': new_report.status.name,
                'owner': {'username': new_report.owner}
            }

        except Exception as ex:
            raise ex
        finally:
            schema.remove_session()
        return out

    @staticmethod
    def new_comment_report(schema: Schema, cid:int, reason: str, owner: str) -> dict:
        """Creates a new report.

        Args:
            - reason (str): The report's reason.
            - schema (Schema): A database handler where the reports are mapped into.
        Returns:
            - dict: A dictionary with the new report's data.
        """

        session: Session = schema.new_session()
        out = {}
        try:
            new_report: ReportComment = ReportsComments.create(session,cid, reason, owner)
            out = {
                'crid': new_report.id,
                'cid': new_report.cid,
                'timestamp': new_report.timestamp,
                'reason' : new_report.reason,
                'status': new_report.status.name,
                'owner': {'username': new_report.owner}
            }

        except Exception as ex:
            raise ex
        finally:
            schema.remove_session()
        return out
