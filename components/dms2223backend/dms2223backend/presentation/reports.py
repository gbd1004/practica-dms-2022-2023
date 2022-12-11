from http import HTTPStatus
import time
from dms2223backend.data.reportstatus import ReportStatus

from flask import current_app

#------------------------#
# BASE DE DATOS TEMPORAL #
#------------------------#


# Definido en: QuestionReportFullModel
REPORTS_Q_DB:dict = {
	1: {
        #'id' : 1, ¿necesario?
        'qrid': 1,
        'qid': 1, # Foreign Key
        'timestamp': 2665574089.0,
        'reason': 'Porque si',
        'status': ReportStatus.ACCEPTED.name,
        'owner':{
            'username' : 'user2'
        }
    },

	2: {
        #'id' : 1, ¿necesario?
        'qrid': 2,
        'qid': 2, # Foreign Key
        'timestamp': 2665574089.0,
        'reason': 'El que ha hecho el post me caia mal',
        'status': ReportStatus.REJECTED.name,
        'owner':{
            'username' : 'user1'
        }
    },

    3: {
        #'id' : 1, ¿necesario?
        'qrid': 3,
        'qid': 2, # Foreign Key
        'timestamp': 2665574089.0,
        'reason': 'Feeling cute, might report later',
        'status': ReportStatus.PENDING.name,
        'owner':{
            'username' : 'user2'
        }
    },	
}

REPORTS_A_DB:dict = {
    1: {
        'arid': 1,
        'aid': 1,
        'timestamp': 2665574089.0,
        'reason': 'Unrelated to the question',
        'status': ReportStatus.PENDING.name,
        'owner':{
            'username' : 'user4'
        }
    },
}

REPORTS_C_DB:dict = {
    1: {
        'crid': 1,
        'cid': 1,
        'timestamp': 2665574089.0,
        'reason': 'Reasons',
        'status': ReportStatus.PENDING.name,
        'owner':{
            'username' : 'user4'
        }
    },
}

#---------------------------------------------------#
# POSIBLES OPERACIONES:     (definidas en spec.yml) #
#---------------------------------------------------#

'''REEPORTS'''
# TODO
def new_question_report(qid: int, body: dict) -> tuple[dict, HTTPStatus]:
	return {"TEMPORAL": 1}, HTTPStatus.OK

# TODO
def new_answer_report(aid: int, body: dict) -> tuple[dict, HTTPStatus]:
	return {"TEMPORAL": 1}, HTTPStatus.OK

# TODO
def new_comment_report(cid: int, body: dict) -> tuple[dict, HTTPStatus]:
	return {"TEMPORAL": 1}, HTTPStatus.OK

# Report GET (list)
def get_questions_reports() -> tuple[dict, HTTPStatus]:
    with current_app.app_context():
	    return REPORTS_Q_DB, HTTPStatus.OK

def get_answers_reports() -> tuple[dict, HTTPStatus]:
    with current_app.app_context():
	    return REPORTS_A_DB, HTTPStatus.OK

def get_comments_reports() -> tuple[dict, HTTPStatus]:
    with current_app.app_context():
        return REPORTS_C_DB, HTTPStatus.OK
	

# Report{rid} POST
# TODO
def set_question_report_status(qrid: int, sentiment: ReportStatus) -> tuple[dict, HTTPStatus]:
	return {"TEMPORAL": 1}, HTTPStatus.OK

# TODO
def set_answer_report_status(arid: int, sentiment: ReportStatus) -> tuple[dict, HTTPStatus]:
	return {"TEMPORAL": 1}, HTTPStatus.OK

# TODO
def set_comment_report_status(crid: int, sentiment: ReportStatus) -> tuple[dict, HTTPStatus]:
	return {"TEMPORAL": 1}, HTTPStatus.OK

