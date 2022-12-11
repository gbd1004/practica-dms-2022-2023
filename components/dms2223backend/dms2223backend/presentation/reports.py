from http import HTTPStatus
from typing import Dict, List
from dms2223backend.data.db import schema
from dms2223backend.data.reportstatus import ReportStatus

from flask import current_app

from dms2223backend.service.reportservice import ReportServices



#---------------------------------------------------#
# POSIBLES OPERACIONES:     (definidas en spec.yml) #
#---------------------------------------------------#

# Report POST
def new_question_report(qid: int, reason: str) -> tuple[dict, HTTPStatus]:
    """Creates a question report

	Returns:
        - Tuple[Dict, HTTPStatus]: A tuple with a dictionary of the report data and a code 200 OK.
    """
    with current_app.app_context():
        # Definido en: QuestionReportFullModel
        new_report: Dict = ReportServices.new_question_report(schema, qid, reason) #TODO: current_app.db) ?
        return new_report, HTTPStatus.OK

# Report POST
def new_answer_report(aid: int, reason: str) -> tuple[dict, HTTPStatus]:
    """Creates an answer report

	Returns:
        - Tuple[Dict, HTTPStatus]: A tuple with a dictionary of the report data and a code 200 OK.
    """
    with current_app.app_context():
        new_report: Dict = ReportServices.new_answer_report(schema, aid, reason) #TODO: current_app.db) ?
        return new_report, HTTPStatus.OK

# Report POST
def new_comment_report(cid: int, reason: str) -> tuple[dict, HTTPStatus]:
    """Creates a comment report

	Returns:
        - Tuple[Dict, HTTPStatus]: A tuple with a dictionary of the report data and a code 200 OK.
    """
    with current_app.app_context():
        new_report: Dict = ReportServices.new_comment_report(schema, cid, reason) #TODO: current_app.db) ?
        return new_report, HTTPStatus.OK




# Report GET (list)
def get_questions_reports() -> tuple[dict, HTTPStatus]:
    """Lists the existing questions reports.

    Returns:
        - Tuple[Dict, HTTPStatus]: A tuple with a dictionary of the reports' data and a code 200 OK.
    """
    with current_app.app_context():
        diccionario: Dict = ReportServices.get_reports_questions(schema) #TODO: current_app.db) ?
        return diccionario, HTTPStatus.OK

# Report GET (list)
def get_answers_reports() -> tuple[dict, HTTPStatus]:
    """Lists the existing answers reports.

    Returns:
        - Tuple[Dict, HTTPStatus]: A tuple with a dictionary of the reports' data and a code 200 OK.
    """
    with current_app.app_context():
        diccionario: Dict = ReportServices.get_reports_answers(schema) #TODO: current_app.db) ?
        return diccionario, HTTPStatus.OK

# Report GET (list)
def get_comments_reports() -> tuple[dict, HTTPStatus]:
    """Lists the existing comments reports.

    Returns:
        - Tuple[Dict, HTTPStatus]: A tuple with a dictionary of the reports' data and a code 200 OK.
    """
    with current_app.app_context():
        diccionario: Dict = ReportServices.get_reports_comments(schema) #TODO: current_app.db) ?
        return diccionario, HTTPStatus.OK
	


# Report{rid} POST
def set_question_report_status(qrid: int, status: ReportStatus) -> tuple[dict, HTTPStatus]:
    """Sets the report's status.

    Returns:
        - Tuple[Dict, HTTPStatus]: A tuple with a dictionary of the reports' data and a code 200 OK.
    """
    with current_app.app_context():
        ReportServices.set_question_report_status(schema, qrid, status)
        report: Dict = ReportServices.get_report_question(schema, qrid)
        return report, HTTPStatus.OK

# Report{rid} POST
def set_answer_report_status(arid: int, status: ReportStatus) -> tuple[dict, HTTPStatus]:
    """Sets the report's status.

    Returns:
        - Tuple[Dict, HTTPStatus]: A tuple with a dictionary of the reports' data and a code 200 OK.
    """
    with current_app.app_context():
        ReportServices.set_answer_report_status(schema, arid, status)
        report: Dict = ReportServices.get_report_answer(schema, arid)
        return report, HTTPStatus.OK

# Report{rid} POST
def set_comment_report_status(crid: int, status: ReportStatus) -> tuple[dict, HTTPStatus]:
    """Sets the report's status.

    Returns:
        - Tuple[Dict, HTTPStatus]: A tuple with a dictionary of the reports' data and a code 200 OK.
    """
    with current_app.app_context():
        ReportServices.set_comment_report_status(schema, crid, status)
        report: Dict = ReportServices.get_report_comment(schema, crid)
        return report, HTTPStatus.OK

