from ast import Dict
from http import HTTPStatus
import time
from flask import current_app
from dms2223backend.data.db import schema
from dms2223backend.service.questionservice import QuestionServices

class QuestionsDB():

	# Constructor
	def __init__(self) -> None:
		pass

	#---------------------------------------------------#
	# POSIBLES OPERACIONES:     (definidas en spec.yml) #
	#---------------------------------------------------#

# Question GET (list)
def get_questions() -> tuple[dict, HTTPStatus]:
	"""Lists the existing questions.

    Returns:
        - Tuple[Dict, HTTPStatus]: A tuple with a dictionary of the questions' data and a code 200 OK.
    """
	with current_app.app_context():
		# Array de objetos: schema QuestionCoreModel
		diccionario: Dict = QuestionServices.get_questions(schema) #TODO: current_app.db) ?

		# Se devuelve la lista
		return diccionario, HTTPStatus.OK


# Question{qid} GET
# Recibe como parámetro: QuestionIdPathParam
def get_question(qid: int) -> tuple[dict, HTTPStatus]:
	"""Gets an existing question with parameter qid.

    Returns:
        - Tuple[Dict, HTTPStatus]: A tuple with a dictionary of the question data and a code 200 OK.
    """
	with current_app.app_context():
		diccionario: Dict = QuestionServices.get_questions(schema) #TODO: current_app.db) ?
		if qid in diccionario:
			return diccionario.get(qid), HTTPStatus.OK
		# Si no existe, no se puede devolver
		return {}, HTTPStatus.NOT_FOUND



# Question POST
def new_question(title: str, body: str) -> tuple[dict, HTTPStatus]:
	"""Creates a question

	Returns:
        - Tuple[Dict, HTTPStatus]: A tuple with a dictionary of the question data and a code 200 OK.
    """
	with current_app.app_context():
		new_question: Dict = QuestionServices.create_question(title, body, schema) #TODO: current_app.db) ?
		return new_question, HTTPStatus.OK



