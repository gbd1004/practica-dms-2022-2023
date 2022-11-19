from http import HTTPStatus
import time
from dms2223backend.data.reportstatus import ReportStatus

from flask import current_app

#------------------------#
# BASE DE DATOS TEMPORAL #
#------------------------#


# Definido en: QuestionReportFullModel
REPORTS_DB = {
	1: {
        #'id' : 1, ¿necesario?
        'qid': 1, # Foreign Key
        'timestamp': 2665574089.0,
        'reason': 'Porque si',
        'status': ReportStatus.ACCEPTED,
        'owner':{
            'username' : 'user2'
        }
    },

	2: {
        #'id' : 1, ¿necesario?
        'qid': 2, # Foreign Key
        'timestamp': 2665574089.0,
        'reason': 'El que ha hecho el post me caia mal',
        'status': ReportStatus.REJECTED,
        'owner':{
            'username' : 'user1'
        }
    },

    3: {
        #'id' : 1, ¿necesario?
        'qid': 2, # Foreign Key
        'timestamp': 2665574089.0,
        'reason': 'Feeling cute, might report later',
        'status': ReportStatus.PENDING,
        'owner':{
            'username' : 'user2'
        }
    },	
}



#---------------------------------------------------#
# POSIBLES OPERACIONES:     (definidas en spec.yml) #
#---------------------------------------------------#


# # Answer{qid} GET (lista)
# # Recibe como parámetro: QuestionIdPathParam
# def get_reports(qid: int):
# 	# Si la prgunta existe, se podrá tratar de obtener sus respuestas
#     lista = []
#     for a in ANSWERS_DB:
#         if ANSWERS_DB[a]['qid'] == qid:
#             lista.append({a:ANSWERS_DB[a]})
#     # Si existen respuestas a la pregunta, se devollverá la pregunta completa
#     if (len(lista) != 0):
#         return lista, HTTPStatus.OK
#     else:
#         return f"No existe una pregunta con identificador {qid}.", HTTPStatus.NOT_FOUND



# # Answer POST
# # Solo es necesario el cuerpo de la pregunta -> schema AnswerCreationModel
# def new_answer(qid:int, body:any):
#     for a in ANSWERS_DB:
#         if ANSWERS_DB[a]['qid'] == qid:
#             lista = []
#             new_id = len(ANSWERS_DB) + 1 # aid = last_aid + 1
#             lista.append({'qid':qid}) # qid
#             lista.append({'timestamp':time.time()}) # current timestamp
#             lista.append({'body':body}) # body
#             #lista.append({'owner': {'username': TO DO}}) # owner
#             lista.append({'votes':0}) # votes (0 por defecto)
#             lista.append({'user_votes':[]}) # vacía
#             #lista.append({'coments': TO DO})
#             ANSWERS_DB[new_id] = lista
#             return ANSWERS_DB.get(new_id), HTTPStatus.CREATED
#     return f"No existe una pregunta con identificador {qid}.", HTTPStatus.NOT_FOUND

# 	# NOTA: 
# 	# ¡Falta obtener usuario propietario! -> schema UserCoreModel: {'username' : string}
# 	# Revisar user_token[] para obtenerlo 



'''REEPORTS'''
# Report POST
def new_report(qid: int):
	pass

# Report GET (list)
def get_reports():
    with current_app.app_context():
	    return REPORTS_DB, HTTPStatus.OK
	

# Report{rid} POST
def set_report_status(rid: int):
	pass

