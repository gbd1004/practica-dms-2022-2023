from http import HTTPStatus
from typing import Dict
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
        new_report: Dict = ReportServices.new_question_report(current_app.db, qid, reason) 
        return new_report, HTTPStatus.OK

# Report POST
def new_answer_report(aid: int, reason: str) -> tuple[dict, HTTPStatus]:
    """Creates an answer report

	Returns:
        - Tuple[Dict, HTTPStatus]: A tuple with a dictionary of the report data and a code 200 OK.
    """
    with current_app.app_context():
        new_report: Dict = ReportServices.new_answer_report(current_app.db, aid, reason)
        return new_report, HTTPStatus.OK

# Report POST
def new_comment_report(cid: int, reason: str) -> tuple[dict, HTTPStatus]:
    """Creates a comment report

	Returns:
        - Tuple[Dict, HTTPStatus]: A tuple with a dictionary of the report data and a code 200 OK.
    """
    with current_app.app_context():
        new_report: Dict = ReportServices.new_comment_report(current_app.db, cid, reason) 
        return new_report, HTTPStatus.OK




# Report GET (list)
def get_questions_reports() -> tuple[dict, HTTPStatus]:
    """Lists the existing questions reports.

    Returns:
        - Tuple[Dict, HTTPStatus]: A tuple with a dictionary of the reports' data and a code 200 OK.
    """
    with current_app.app_context():
        diccionario: Dict = ReportServices.get_reports_questions(current_app.db) 
        return diccionario, HTTPStatus.OK

# Report GET (list)
def get_answers_reports() -> tuple[dict, HTTPStatus]:
    """Lists the existing answers reports.

    Returns:
        - Tuple[Dict, HTTPStatus]: A tuple with a dictionary of the reports' data and a code 200 OK.
    """
    with current_app.app_context():
        diccionario: Dict = ReportServices.get_reports_answers(current_app.db) 
        return diccionario, HTTPStatus.OK

# Report GET (list)
def get_comments_reports() -> tuple[dict, HTTPStatus]:
    """Lists the existing comments reports.

    Returns:
        - Tuple[Dict, HTTPStatus]: A tuple with a dictionary of the reports' data and a code 200 OK.
    """
    with current_app.app_context():
        diccionario: Dict = ReportServices.get_reports_comments(current_app.db) 
        return diccionario, HTTPStatus.OK
	


# Report{rid} POST
def set_question_report_status(qrid: int, status: ReportStatus) -> tuple[dict, HTTPStatus]:
    """Sets the report's status.

    Returns:
        - Tuple[Dict, HTTPStatus]: A tuple with a dictionary of the reports' data and a code 200 OK.
    """
    with current_app.app_context():
        ReportServices.set_question_report_status(current_app.db, qrid, status)
        report: Dict = ReportServices.get_report_question(current_app.db, qrid)
        return report, HTTPStatus.OK

# Report{rid} POST
def set_answer_report_status(arid: int, status: ReportStatus) -> tuple[dict, HTTPStatus]:
    """Sets the report's status.

    Returns:
        - Tuple[Dict, HTTPStatus]: A tuple with a dictionary of the reports' data and a code 200 OK.
    """
    with current_app.app_context():
        ReportServices.set_answer_report_status(current_app.db, arid, status)
        report: Dict = ReportServices.get_report_answer(current_app.db, arid)
        return report, HTTPStatus.OK

# Report{rid} POST
def set_comment_report_status(crid: int, status: ReportStatus) -> tuple[dict, HTTPStatus]:
    """Sets the report's status.

    Returns:
        - Tuple[Dict, HTTPStatus]: A tuple with a dictionary of the reports' data and a code 200 OK.
    """
    with current_app.app_context():
        ReportServices.set_comment_report_status(current_app.db, crid, status)
        report: Dict = ReportServices.get_report_comment(current_app.db, crid)
        return report, HTTPStatus.OK

