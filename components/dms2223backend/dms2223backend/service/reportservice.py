""" 
ReportServices class module.
"""

from ast import Dict
from typing import List
from sqlalchemy.orm.session import Session
from dms2223backend.data.db.results.answerdb import Answer
from dms2223backend.data.db.results.commentdb import Comment
from dms2223backend.data.db.results.questiondb import Question
from dms2223backend.data.db.results.report.reportanswerdb import ReportAnswer
from dms2223backend.data.db.results.report.reportcommentdb import ReportComment
from dms2223backend.data.db.results.report.reportdb import Report
from dms2223backend.data.db.results.report.reportquestiondb import ReportQuestion
from dms2223backend.data.db.resultsets.answersdb import Answers
from dms2223backend.data.db.resultsets.commentsdb import Comments
from dms2223backend.data.db.resultsets.questionsdb import Questions
from dms2223backend.data.db.resultsets.reports.reportsanswersdb import ReportsAnswer
from dms2223backend.data.db.resultsets.reports.reportscommentsdb import ReportsComments
from dms2223backend.data.db.resultsets.reports.reportsquestionsdb import ReportsQuestions
from dms2223backend.data.db.schema import Schema
from dms2223backend.data.db.results.commentdb import Comment
from dms2223backend.data.reportstatus import ReportStatus
from dms2223backend.service.answerservice import AnswerServices
from dms2223backend.service.commentservice import CommentServices
from dms2223backend.service.questionservice import QuestionServices


class ReportServices():
    """ 
    Monostate class that provides high-level services to handle Reports' use cases.
    """

    @staticmethod
    def get_reports_questions(schema: Schema) -> List[Dict]:
        """Lists the existing reports.

        Args:
            - schema (Schema): A database handler where the reports are mapped into.

        Returns:
            - List[Dict]: A list of dictionaries with the reports' data.
        """
        out: List[Dict] = []
        session: Session = schema.new_session()
        reports: List[ReportQuestion] = ReportsQuestions.list_all(session)
        for r in reports:
            out.append({
                'qrid': r.id,
                'qid': r.eid,
                'timestamp': r.timestamp,
                'reason' : r.reason,
                'status': r.status,
                'owner': {'username': r.owner}
                })
        schema.remove_session()
        return out

    staticmethod
    def get_reports_answers(schema: Schema) -> List[Dict]:
        """Lists the existing reports.

        Args:
            - schema (Schema): A database handler where the reports are mapped into.

        Returns:
            - List[Dict]: A list of dictionaries with the reports' data.
        """
        out: List[Dict] = []
        session: Session = schema.new_session()
        reports: List[ReportAnswer] = ReportsAnswer.list_all(session)
        for r in reports:
            out.append({
                'arid': r.id,
                'aid': r.eid,
                'timestamp': r.timestamp,
                'reason' : r.reason,
                'status': r.status,
                'owner': {'username': r.owner}
                })
        schema.remove_session()
        return out

    
    staticmethod
    def get_reports_comments(schema: Schema) -> List[Dict]:
        """Lists the existing reports.

        Args:
            - schema (Schema): A database handler where the reports are mapped into.

        Returns:
            - List[Dict]: A list of dictionaries with the reports' data.
        """
        out: List[Dict] = []
        session: Session = schema.new_session()
        reports: List[ReportComment] = ReportsComments.list_all(session)
        for r in reports:
            out.append({
                'crid': r.id,
                'cid': r.eid,
                'timestamp': r.timestamp,
                'reason' : r.reason,
                'status': r.status,
                'owner': {'username': r.owner}
                })
        schema.remove_session()
        return out

    @staticmethod
    def set_question_report_status(schema: Schema, qrid: int, status: ReportStatus):
        """Changes the status of the report

        Args:
            - qrid (int): The report's id.
            - schema (Schema): A database handler where the reports are mapped into.
        
        """
        session: Session = schema.new_session()
        
        report: ReportQuestion = ReportsQuestions.get_report(session, qrid)

        report.status = status
        if status.name == 'ACCEPTED':
            QuestionServices.hide_question(schema, report.qid)

        # Actualizamos el reporte
        session.add(report)
        session.commit()

        schema.remove_session()
    
    @staticmethod
    def set_answer_report_status(schema: Schema, arid: int, status: ReportStatus):
        """Changes the status of the report

        Args:
            - arid (int): The report's id.
            - schema (Schema): A database handler where the reports are mapped into.
        
        """
        session: Session = schema.new_session()
        
        report: ReportAnswer = ReportsAnswer.get_report(session, arid)

        report.status = status
        if status.name == 'ACCEPTED':
            AnswerServices.hide_answer(schema, report.aid)

        # Actualizamos el reporte
        session.add(report)
        session.commit()

        schema.remove_session()

    @staticmethod
    def set_comment_report_status(schema: Schema, crid: int, status: ReportStatus):
        """Changes the status of the report

        Args:
            - crid (int): The report's id.
            - schema (Schema): A database handler where the reports are mapped into.
        
        """
        session: Session = schema.new_session()
        
        report: ReportComment = ReportsComments.get_report(session, crid)

        report.status = status
        if status.name == 'ACCEPTED':
            CommentServices.hide_comment(schema, report.id)

        # Actualizamos el reporte
        session.add(report)
        session.commit()

        schema.remove_session()


    @staticmethod
    def new_question_report(schema: Schema, reason: str) -> Dict:
        """Creates a new report.

        Args:
            - reason (str): The report's reason.
            - schema (Schema): A database handler where the reports are mapped into.

        Returns:
            - Dict: A dictionary with the new report's data.
        """

        session: Session = schema.new_session()
        out: Dict = {}
        try:
            new_report: ReportQuestion = ReportsQuestions.create(session, reason)
            out['qrid'] = {
                    'qrid': new_report.id,
                    'qid': new_report.qid,
                    'timestamp': new_report.timestamp,
                    'reason' : new_report.reason,
                    'status': new_report.status,
                    'owner': {'username': new_report.owner}
            }
            
        except Exception as ex:
            raise ex
        finally:
            schema.remove_session()
        return out

    @staticmethod
    def new_answer_report(schema: Schema, reason: str) -> Dict:
        """Creates a new report.

        Args:
            - reason (str): The report's reason.
            - schema (Schema): A database handler where the reports are mapped into.

        Returns:
            - Dict: A dictionary with the new report's data.
        """

        session: Session = schema.new_session()
        out: Dict = {}
        try:
            new_report: ReportAnswer = ReportsAnswer.create(session, reason)
            out['arid'] = {
                    'arid': new_report.id,
                    'aid': new_report.aid,
                    'timestamp': new_report.timestamp,
                    'reason' : new_report.reason,
                    'status': new_report.status,
                    'owner': {'username': new_report.owner}
            }
            
        except Exception as ex:
            raise ex
        finally:
            schema.remove_session()
        return out
    
    @staticmethod
    def new_comment_report(schema: Schema, reason: str) -> Dict:
        """Creates a new report.

        Args:
            - reason (str): The report's reason.
            - schema (Schema): A database handler where the reports are mapped into.

        Returns:
            - Dict: A dictionary with the new report's data.
        """

        session: Session = schema.new_session()
        out: Dict = {}
        try:
            new_report: ReportComment = ReportsComments.create(session, reason)
            out['crid'] = {
                    'crid': new_report.id,
                    'cid': new_report.cid,
                    'timestamp': new_report.timestamp,
                    'reason' : new_report.reason,
                    'status': new_report.status,
                    'owner': {'username': new_report.owner}
            }
            
        except Exception as ex:
            raise ex
        finally:
            schema.remove_session()
        return out




   