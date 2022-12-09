from http import HTTPStatus
import time

from flask import current_app

class QuestionsDB():

	# Constructor
	def __init__(self) -> None:
		pass

	#------------------------#
	# BASE DE DATOS TEMPORAL #
	#------------------------#

	# Definido en: schema QuestionFullModel
QUESTIONS_DB = {

	1: {
		'qid': 1,
		'title': 'Pregunta1',
		'body': 'Contenido1',
		'timestamp': 1665574089.0,
		'owner': {
				'username': 'user1'
		}
		
	},

	2: {
		'qid': 2,
		'title': 'Pregunta2',
		'body': 'Contenido2',
		'timestamp': 1665693009.12,
		'owner': {
				'username': 'user2'
		}
	}

}


	#---------------------------------------------------#
	# POSIBLES OPERACIONES:     (definidas en spec.yml) #
	#---------------------------------------------------#

# Question GET (list)
# def get_questions(self):
# 	# Array de objetos: schema QuestionCoreModel
# 	lista = []
# 	for q in self.QUESTIONS_DB.values():
# 		lista.append['qid']
# 		lista.append['title']
# 		lista.append['timestamp']
# 	# Se devuelve la lista
# 	return {'questions': lista}, HTTPStatus.OK
def get_questions() -> tuple[dict, HTTPStatus]:
	with current_app.app_context():
		return QUESTIONS_DB, HTTPStatus.OK


# Question POST
def new_question() -> tuple[dict, HTTPStatus]:
	return {"TEMPORAL": 1}, HTTPStatus.OK

	# NOTA: el parámetro entrada 'body' deberá tener: 
	# Schema QuestionCreationModel: {title, body}
	# ¡Falta obtener usuario propietario! -> schema UserCoreModel: {'username' : string}
	# Revisar user_token[] para obtenerlo


# Question{qid} GET
# Recibe como parámetro: QuestionIdPathParam
def get_question(qid: int):
	# Si existe, la obtenemos
	if qid in QUESTIONS_DB:
		return QUESTIONS_DB.get(qid), HTTPStatus.OK
	# Si no existe, no se puede devolver
	return {}, HTTPStatus.NOT_FOUND

