from http import HTTPStatus
from typing import Dict
from flask import current_app
from dms2223backend.service.reportservice import ReportServices

#---------------------------------------------------#
# POSIBLES OPERACIONES:     (definidas en spec.yml) #
#---------------------------------------------------#

# Report POST
def new_question_report(qid: int, body: dict, token_info: dict) -> tuple[dict, HTTPStatus]:
    """Creates a question report

    Returns:
        - Tuple[Dict, HTTPStatus]: A tuple with a dictionary of the report data and a code 200.
    """
    with current_app.app_context():
        # Definido en: QuestionReportFullModel
        owner = token_info['user_token']['username']
        new_report: Dict = ReportServices.new_question_report(
            current_app.db, qid, body['reason'], owner
        )
        return new_report, HTTPStatus.OK

# Report POST
def new_answer_report(aid: int, body: dict, token_info: dict) -> tuple[dict, HTTPStatus]:
    """Creates an answer report

    Returns:
        - Tuple[Dict, HTTPStatus]: A tuple with a dictionary of the report data and a code 200.
    """
    with current_app.app_context():
        owner = token_info['user_token']['username']
        new_report: Dict = ReportServices.new_answer_report(
            current_app.db, aid, body['reason'], owner
        )
        return new_report, HTTPStatus.OK

# Report POST
def new_comment_report(cid: int, body: dict, token_info: dict) -> tuple[dict, HTTPStatus]:
    """Creates a comment report

    Returns:
        - Tuple[Dict, HTTPStatus]: A tuple with a dictionary of the report data and a code 200.
    """
    with current_app.app_context():
        owner = token_info['user_token']['username']
        new_report: Dict = ReportServices.new_comment_report(
            current_app.db, cid, body['reason'], owner
        )
        return new_report, HTTPStatus.OK

# Report GET (list)
def get_questions_reports() -> tuple[list, HTTPStatus]:
    """Lists the existing questions reports.

    Returns:
        - Tuple[Dict, HTTPStatus]: A tuple with a dictionary of the reports' data and a code 200.
    """
    with current_app.app_context():
        diccionario: list = ReportServices.get_reports_questions(current_app.db)
        current_app.logger.info(diccionario)
        return diccionario, HTTPStatus.OK

# Report GET (list)
def get_answers_reports() -> tuple[list, HTTPStatus]:
    """Lists the existing answers reports.

    Returns:
        - Tuple[Dict, HTTPStatus]: A tuple with a dictionary of the reports' data and a code 200.
    """
    with current_app.app_context():
        diccionario: list = ReportServices.get_reports_answers(current_app.db)
        return diccionario, HTTPStatus.OK

# Report GET (list)
def get_comments_reports() -> tuple[list, HTTPStatus]:
    """Lists the existing comments reports.

    Returns:
        - Tuple[Dict, HTTPStatus]: A tuple with a dictionary of the reports' data and a code 200.
    """
    with current_app.app_context():
        diccionario: list = ReportServices.get_reports_comments(current_app.db)
        return diccionario, HTTPStatus.OK

# Report{rid} POST
def set_question_report_status(qrid: int, body: dict) -> tuple[dict, HTTPStatus]:
    """Sets the report's status.

    Returns:
        - Tuple[Dict, HTTPStatus]: A tuple with a dictionary of the reports' data and a code 200.
    """
    with current_app.app_context():
        ReportServices.set_question_report_status(current_app.db, qrid, body['status'])
        report: Dict = ReportServices.get_report_question(current_app.db, qrid)
        return report, HTTPStatus.OK

# Report{rid} POST
def set_answer_report_status(arid: int, body: dict) -> tuple[dict, HTTPStatus]:
    """Sets the report's status.

    Returns:
        - Tuple[Dict, HTTPStatus]: A tuple with a dictionary of the reports' data and a code 200.
    """
    with current_app.app_context():
        ReportServices.set_answer_report_status(current_app.db, arid, body['status'])
        report: Dict = ReportServices.get_report_answer(current_app.db, arid)
        return report, HTTPStatus.OK

# Report{rid} POST
def set_comment_report_status(crid: int, body: dict) -> tuple[dict, HTTPStatus]:
    """Sets the report's status.

    Returns:
        - Tuple[Dict, HTTPStatus]: A tuple with a dictionary of the reports' data and a code 200.
    """
    with current_app.app_context():
        ReportServices.set_comment_report_status(current_app.db, crid, body['status'])
        report: Dict = ReportServices.get_report_comment(current_app.db, crid)
        return report, HTTPStatus.OK
